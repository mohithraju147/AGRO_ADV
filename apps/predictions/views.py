from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import requests

from apps.farmers.models import Farmer
from apps.crops.models import Crop
from apps.market.models import MarketPrice
from apps.schemes.models import Scheme
from apps.predictions.models import Prediction
from apps.predictions.ml_engine import predict_crop, calculate_profit
from apps.predictions.translations import get_ui

STATES = ['Andhra Pradesh','Assam','Bihar','Chhattisgarh','Gujarat','Haryana',
    'Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh',
    'Maharashtra','Odisha','Punjab','Rajasthan','Tamil Nadu','Telangana',
    'Uttar Pradesh','Uttarakhand','West Bengal']

def get_lang(request):
    if request.GET.get('lang'):
        request.session['lang'] = request.GET['lang']
    return request.session.get('lang', 'en')

def get_farmer(request):
    fid = request.session.get('farmer_id')
    if fid:
        try: return Farmer.objects.get(pk=fid)
        except Farmer.DoesNotExist: pass
    return None

def ctx(request):
    return {'lang': get_lang(request), 'ui': get_ui(get_lang(request))}

def home(request):
    c = ctx(request)
    recent = Prediction.objects.select_related('farmer').order_by('-created_at')[:6]
    for p in recent: p.confidence_pct = round(p.confidence * 100)
    c.update({'farmer': get_farmer(request), 'recent': recent,
        'total_preds': Prediction.objects.count(), 'total_schemes': Scheme.objects.count()})
    return render(request, 'base/home.html', c)

def login_page(request):
    if get_farmer(request):
        return redirect('predict')
    c = ctx(request)
    return render(request, 'farmers/login.html', c)

def login_verify(request):
    mobile = request.GET.get('mobile', '').strip()
    if not mobile:
        return redirect('login')
    try:
        farmer = Farmer.objects.get(mobile=mobile)
        request.session['farmer_id'] = farmer.id
        messages.success(request, f'Welcome back, {farmer.name}! 👋')
        return redirect('predict')
    except Farmer.DoesNotExist:
        messages.error(request, 'Profile not found. Please register.')
        return redirect('farmer_profile')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def farmer_profile(request):
    c = ctx(request)
    farmer = get_farmer(request)
    if request.method == 'POST':
        mobile = request.POST.get('mobile','').strip()
        data = {k: request.POST.get(k,'').strip() for k in ['name','street','area','district','state','pincode']}
        data['mobile'] = mobile
        data['farm_size'] = request.POST.get('farm_size','1')
        if not data['name'] or not mobile or not data['district'] or not data['state']:
            messages.error(request, 'Please fill all required fields.')
            c.update({'farmer': farmer, 'states': STATES})
            return render(request, 'farmers/profile.html', c)
        farmer, created = Farmer.objects.update_or_create(mobile=mobile, defaults=data)
        messages.success(request, f"{'Profile created' if created else 'Profile updated'}! Welcome, {farmer.name}.")
        request.session['farmer_id'] = farmer.id
        return redirect('predict')
    c.update({'farmer': farmer, 'states': STATES})
    return render(request, 'farmers/profile.html', c)

def predict(request):
    c = ctx(request)
    farmer = get_farmer(request)
    if request.method == 'POST':
        if not farmer:
            messages.error(request, 'Please create your profile first.')
            return redirect('farmer_profile')
        try:
            soil_type   = request.POST.get('soil_type','loamy')
            ph_value    = float(request.POST.get('ph_value',6.5))
            nitrogen    = float(request.POST.get('nitrogen',60))
            phosphorus  = float(request.POST.get('phosphorus',40))
            potassium   = float(request.POST.get('potassium',40))
            temperature = float(request.POST.get('temperature',25))
            humidity    = float(request.POST.get('humidity',65))
            rainfall    = float(request.POST.get('rainfall',800))
            user_state  = request.POST.get('user_state', farmer.state)
            user_dist   = request.POST.get('user_district', farmer.district)
        except (ValueError, TypeError):
            messages.error(request, 'Invalid values. Please enter correct numbers.')
            c.update({'farmer': farmer}); return render(request, 'predictions/predict.html', c)
        result = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall)
        profit = calculate_profit(result['crop_name'], farmer.farm_size)
        pred = Prediction.objects.create(
            farmer=farmer, soil_type=soil_type, ph_value=ph_value,
            nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
            temperature=temperature, humidity=humidity, rainfall=rainfall,
            crop_name=result['crop_name'], confidence=result['confidence'],
            top3_crops=result['top3'], reason=result['reason'],
            seed_cost=profit['seed_cost'], fertilizer=profit['fertilizer'],
            labour_cost=profit['labour_cost'], expected_rev=profit['expected_rev'],
            net_profit=profit['net_profit'],
        )
        request.session['last_pred_id'] = pred.id
        request.session['pred_state']   = user_state
        request.session['pred_district']= user_dist
        return redirect('results')
    c.update({'farmer': farmer})
    return render(request, 'predictions/predict.html', c)

def results(request):
    c = ctx(request)
    pid = request.session.get('last_pred_id')
    if not pid: return redirect('predict')
    try: pred = Prediction.objects.select_related('farmer').get(pk=pid)
    except Prediction.DoesNotExist: return redirect('predict')
    user_state = request.session.get('pred_state', pred.farmer.state)
    user_dist  = request.session.get('pred_district', pred.farmer.district)
    market_price = (
        MarketPrice.objects.filter(crop_name__icontains=pred.crop_name, state=user_state).first()
        or MarketPrice.objects.filter(crop_name__icontains=pred.crop_name).first()
    )
    nearby  = MarketPrice.objects.filter(state=user_state).order_by('crop_name')[:15]
    schemes = Scheme.objects.filter(Q(state='') | Q(state=user_state))[:6]
    profit  = calculate_profit(pred.crop_name, pred.farmer.farm_size)
    history = Prediction.objects.filter(farmer=pred.farmer).order_by('-created_at')[:5]
    c.update({'pred': pred, 'market_price': market_price, 'nearby': nearby,
        'schemes': schemes, 'profit': profit, 'history': history,
        'conf_pct': round(pred.confidence * 100), 'top3': pred.top3_crops,
        'user_state': user_state, 'user_dist': user_dist})
    return render(request, 'predictions/results.html', c)

def market(request):
    c = ctx(request)
    search=request.GET.get('q',''); category=request.GET.get('category',''); state=request.GET.get('state','')
    prices = MarketPrice.objects.all()
    if search:   prices = prices.filter(crop_name__icontains=search)
    if category: prices = prices.filter(category=category)
    if state:    prices = prices.filter(state=state)
    states = MarketPrice.objects.values_list('state',flat=True).distinct().order_by('state')
    c.update({'prices':prices,'search':search,'category':category,'state':state,'states':states,
        'grains':MarketPrice.objects.filter(category='grain').count(),
        'vegs':MarketPrice.objects.filter(category='vegetable').count(),
        'fruits':MarketPrice.objects.filter(category='fruit').count(),
        'total':MarketPrice.objects.count()})
    return render(request, 'market/market.html', c)

def encyclopedia(request):
    c = ctx(request)
    search=request.GET.get('q',''); crop_id=request.GET.get('id'); sel=None
    crops = Crop.objects.all()
    if search: crops = crops.filter(Q(name__icontains=search)|Q(local_name__icontains=search))
    if crop_id:
        try: sel = Crop.objects.get(pk=crop_id)
        except Crop.DoesNotExist: pass
    c.update({'crops':crops,'sel':sel,'search':search})
    return render(request, 'crops/encyclopedia.html', c)

def schemes(request):
    c = ctx(request)
    search=request.GET.get('q',''); state=request.GET.get('state','')
    qs = Scheme.objects.all()
    if search: qs = qs.filter(Q(title__icontains=search)|Q(description__icontains=search))
    if state=='national': qs = qs.filter(state='')
    elif state: qs = qs.filter(Q(state=state)|Q(state=''))
    all_states = Scheme.objects.exclude(state='').values_list('state',flat=True).distinct().order_by('state')
    c.update({'schemes':qs,'search':search,'state':state,'all_states':all_states})
    return render(request, 'schemes/schemes.html', c)

def history(request):
    c = ctx(request)
    farmer = get_farmer(request)
    if not farmer: return redirect('farmer_profile')
    preds = Prediction.objects.filter(farmer=farmer).order_by('-created_at')
    for p in preds: p.confidence_pct = round(p.confidence * 100)
    c.update({'farmer':farmer,'predictions':preds})
    return render(request, 'predictions/history.html', c)

def geocode_api(request):
    lat=request.GET.get('lat'); lon=request.GET.get('lon')
    if not lat or not lon: return JsonResponse({'error':'lat and lon required'},status=400)
    try:
        url=f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        r=requests.get(url,headers={'User-Agent':'AGRO_ADV/1.0'},timeout=6)
        d=r.json(); addr=d.get('address',{})
        state_map={'Karnataka':'Karnataka','Tamil Nadu':'Tamil Nadu','Tamilnadu':'Tamil Nadu',
            'Maharashtra':'Maharashtra','Gujarat':'Gujarat','Rajasthan':'Rajasthan',
            'Uttar Pradesh':'Uttar Pradesh','Madhya Pradesh':'Madhya Pradesh',
            'Andhra Pradesh':'Andhra Pradesh','Telangana':'Telangana','Punjab':'Punjab',
            'Haryana':'Haryana','Bihar':'Bihar','West Bengal':'West Bengal',
            'Odisha':'Odisha','Assam':'Assam','Kerala':'Kerala','Jharkhand':'Jharkhand',
            'Chhattisgarh':'Chhattisgarh','Himachal Pradesh':'Himachal Pradesh','Uttarakhand':'Uttarakhand'}
        state=state_map.get(addr.get('state',''),addr.get('state',''))
        return JsonResponse({'area':addr.get('suburb') or addr.get('neighbourhood') or addr.get('village') or addr.get('town',''),
            'district':addr.get('county') or addr.get('city_district') or addr.get('city',''),
            'state':state,'country':addr.get('country','India'),'pincode':addr.get('postcode','')})
    except Exception as e:
        return JsonResponse({'error':str(e)},status=503)
