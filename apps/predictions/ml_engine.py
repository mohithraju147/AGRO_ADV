import joblib, numpy as np
from pathlib import Path
from django.conf import settings

_model=None; _encoder=None

REASONS = {
    'rice':'High rainfall and humidity suit paddy cultivation perfectly.',
    'wheat':'Cool temperature and moderate rainfall are ideal for wheat.',
    'maize':'Warm climate with moderate water availability suits maize.',
    'cotton':'High temperature and well-drained soil are perfect for cotton.',
    'chickpea':'Low rainfall and cool dry climate are optimal for chickpea.',
    'kidneybeans':'Moderate temperature and good soil moisture suit kidney beans.',
    'pigeonpeas':'Warm temperature with moderate rainfall is ideal for pigeon peas.',
    'mothbeans':'Hot dry climate with sandy soil is perfect for moth beans.',
    'mungbean':'Warm humid conditions are well suited for mung beans.',
    'blackgram':'Warm climate with adequate moisture suits black gram.',
    'lentil':'Cool dry climate with moderate nutrients is ideal for lentil.',
    'pomegranate':'Warm dry climate with well-drained soil suits pomegranate.',
    'banana':'Tropical humid climate is perfect for banana cultivation.',
    'mango':'Warm dry season followed by monsoon is ideal for mango.',
    'grapes':'Moderate climate with well-drained soil suits grapes.',
    'watermelon':'Hot dry climate with sandy loam soil is perfect for watermelon.',
    'muskmelon':'Warm dry climate with light soil is ideal for muskmelon.',
    'apple':'Cool hilly climate with moderate rainfall suits apple orchards.',
    'orange':'Subtropical climate with moderate rainfall is ideal for oranges.',
    'papaya':'Warm tropical climate with rich soil suits papaya.',
    'coconut':'Coastal tropical climate with high humidity is perfect for coconut.',
    'jute':'Hot humid climate with alluvial soil is ideal for jute.',
    'coffee':'Cool humid tropical climate suits coffee perfectly.',
}

COSTS = {
    'rice':       {'seed':3000,'fert':5000,'labour':8000, 'yield':25, 'price':1800},
    'wheat':      {'seed':4000,'fert':4500,'labour':6000, 'yield':30, 'price':2015},
    'maize':      {'seed':2500,'fert':4000,'labour':5000, 'yield':28, 'price':1700},
    'cotton':     {'seed':5000,'fert':8000,'labour':12000,'yield':15, 'price':6500},
    'chickpea':   {'seed':3500,'fert':3000,'labour':5000, 'yield':14, 'price':5200},
    'kidneybeans':{'seed':4000,'fert':3500,'labour':5500, 'yield':12, 'price':7000},
    'pigeonpeas': {'seed':3000,'fert':3000,'labour':5000, 'yield':10, 'price':6000},
    'mothbeans':  {'seed':2000,'fert':2500,'labour':4000, 'yield':8,  'price':5500},
    'mungbean':   {'seed':2500,'fert':2500,'labour':4000, 'yield':8,  'price':7000},
    'blackgram':  {'seed':2500,'fert':3000,'labour':4500, 'yield':9,  'price':6500},
    'lentil':     {'seed':3000,'fert':2500,'labour':4000, 'yield':10, 'price':5800},
    'pomegranate':{'seed':8000,'fert':6000,'labour':10000,'yield':80, 'price':6500},
    'banana':     {'seed':6000,'fert':8000,'labour':12000,'yield':300,'price':1500},
    'mango':      {'seed':5000,'fert':6000,'labour':10000,'yield':80, 'price':2800},
    'grapes':     {'seed':10000,'fert':8000,'labour':15000,'yield':120,'price':5000},
    'watermelon': {'seed':2000,'fert':4000,'labour':6000, 'yield':200,'price':500},
    'muskmelon':  {'seed':2000,'fert':4000,'labour':6000, 'yield':150,'price':800},
    'apple':      {'seed':12000,'fert':8000,'labour':15000,'yield':100,'price':8000},
    'orange':     {'seed':6000,'fert':5000,'labour':8000, 'yield':100,'price':4000},
    'papaya':     {'seed':2000,'fert':5000,'labour':8000, 'yield':200,'price':800},
    'coconut':    {'seed':5000,'fert':4000,'labour':6000, 'yield':60, 'price':15000},
    'jute':       {'seed':2500,'fert':4000,'labour':8000, 'yield':20, 'price':4500},
    'coffee':     {'seed':8000,'fert':6000,'labour':12000,'yield':8,  'price':35000},
    'default':    {'seed':3000,'fert':5000,'labour':7000, 'yield':20, 'price':2000},
}

def load_model():
    global _model,_encoder
    if _model is None:
        mp=settings.ML_MODEL_PATH; ep=settings.ML_ENCODER_PATH
        if Path(mp).exists() and Path(ep).exists():
            _model=joblib.load(mp); _encoder=joblib.load(ep)
    return _model,_encoder

def predict_crop(N,P,K,temperature,humidity,ph,rainfall):
    model,encoder=load_model()
    if model is None:
        return _fallback(temperature,rainfall,ph,humidity)
    feat=np.array([[N,P,K,temperature,humidity,ph,rainfall]])
    proba=model.predict_proba(feat)[0]
    top3=np.argsort(proba)[::-1][:3]
    crop=encoder.inverse_transform([top3[0]])[0]
    conf=float(proba[top3[0]])
    top3_list=[{'crop':encoder.inverse_transform([i])[0],'confidence':round(float(proba[i])*100,1)} for i in top3]
    reason=REASONS.get(crop,f'Based on soil nutrients, pH {ph}, temperature {temperature}°C and rainfall {rainfall}mm, {crop.title()} is most suitable.')
    return {'crop_name':crop,'confidence':round(conf,4),'top3':top3_list,'reason':reason}

def _fallback(temperature,rainfall,ph,humidity):
    if rainfall>1500 and humidity>75: crop='rice'
    elif temperature<20 and rainfall<800: crop='wheat'
    elif temperature>30 and rainfall<500: crop='cotton'
    elif rainfall<400 and temperature<28: crop='chickpea'
    elif humidity>80 and temperature>25: crop='banana'
    else: crop='maize'
    return {'crop_name':crop,'confidence':0.72,'top3':[{'crop':crop,'confidence':72.0}],'reason':REASONS.get(crop,f'{crop.title()} suits your conditions.')}

def calculate_profit(crop_name,farm_size):
    c=COSTS.get(crop_name.lower(),COSTS['default'])
    fs=float(farm_size)
    seed=round(c['seed']*fs,2); fert=round(c['fert']*fs,2); labour=round(c['labour']*fs,2)
    total=round(seed+fert+labour,2); rev=round(c['yield']*c['price']*fs,2); profit=round(rev-total,2)
    roi=round((profit/total)*100,1) if total>0 else 0
    return {'seed_cost':seed,'fertilizer':fert,'labour_cost':labour,'total_cost':total,'expected_rev':rev,'net_profit':profit,'roi':roi}
