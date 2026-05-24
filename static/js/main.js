document.addEventListener('DOMContentLoaded',function(){
  const soilHints={alluvial:{N:80,P:50,K:50,note:'Alluvial — high fertility, river plains. Most crops thrive.'},black:{N:70,P:45,K:60,note:'Black/Regur — high clay. Good for cotton, sorghum.'},red:{N:50,P:35,K:40,note:'Red soil — low fertility. Needs extra nutrients.'},laterite:{N:45,P:30,K:35,note:'Laterite — acidic, leached. Good for cashew, coffee.'},sandy:{N:40,P:25,K:30,note:'Sandy — well-drained, low retention. Frequent irrigation needed.'},loamy:{N:75,P:50,K:50,note:'Loamy — ideal balance. Most versatile for all crops.'}};
  const ss=document.getElementById('soil_type'),hd=document.getElementById('soil_hint'),ni=document.getElementById('nitrogen'),pi=document.getElementById('phosphorus'),ki=document.getElementById('potassium');
  if(ss){ss.addEventListener('change',function(){const h=soilHints[this.value];if(!h)return;if(hd){hd.className='alert alert-success py-2 px-3 mt-2 small border-0';hd.innerHTML='<i class="fas fa-info-circle me-2"></i>'+h.note;}if(ni&&!ni._t)ni.value=h.N;if(pi&&!pi._t)pi.value=h.P;if(ki&&!ki._t)ki.value=h.K;});[ni,pi,ki].forEach(function(i){if(i)i.addEventListener('input',function(){this._t=true;});}); }
  const ph=document.getElementById('ph_value'),pb=document.getElementById('ph_bar'),pl=document.getElementById('ph_label');
  if(ph&&pb){function uPH(){const v=parseFloat(ph.value)||6.5;pb.style.width=(((v-4)/5)*100)+'%';let col,lab;if(v<5.5){col='#ef4444';lab='Very Acidic';}else if(v<6.5){col='#f59e0b';lab='Slightly Acidic';}else if(v<=7.5){col='#10b981';lab='Neutral — Ideal';}else if(v<=8.0){col='#3b82f6';lab='Slightly Alkaline';}else{col='#8b5cf6';lab='Very Alkaline';}pb.style.background=col;if(pl)pl.innerHTML='<span style="color:'+col+'">'+v+' — '+lab+'</span>';}ph.addEventListener('input',uPH);uPH();}
  const cf=document.getElementById('conf_fill');if(cf)setTimeout(()=>{cf.style.width=cf.dataset.pct+'%';},400);
  const pc=document.getElementById('profitChart');
  if(pc){const d=pc.dataset;new Chart(pc,{type:'bar',data:{labels:['Seeds','Fertilizer','Labour','Total Cost','Revenue','Net Profit'],datasets:[{data:[+d.seed,+d.fert,+d.labour,+d.total,+d.rev,+d.profit],backgroundColor:['#74c69d','#52b788','#40916c','#1a4731','#e9a825','#2d6a4f'],borderRadius:8,borderSkipped:false}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>'₹'+parseInt(v).toLocaleString('en-IN')},grid:{color:'#f0f0f0'}},x:{grid:{display:false}}}}});}
  const mc=document.getElementById('marketChart');
  if(mc){const labels=JSON.parse(mc.dataset.labels||'[]'),prices=JSON.parse(mc.dataset.prices||'[]');new Chart(mc,{type:'bar',data:{labels,datasets:[{label:'Modal Price',data:prices,backgroundColor:'#40916c',borderRadius:6,hoverBackgroundColor:'#2d6a4f'}]},options:{responsive:true,plugins:{legend:{display:false}},spaces:{y:{ticks:{callback:v=>'₹'+parseInt(v).toLocaleString('en-IN')},grid:{color:'#f0f0f0'}},x:{grid:{display:false},ticks:{font:{size:11}}}}}});}
});

function detectLocation(){
  const btn=document.getElementById('detectBtn');
  const loading=document.getElementById('loc_loading');
  const result=document.getElementById('loc_result');
  const errDiv=document.getElementById('loc_error');
  if(!navigator.geolocation){errDiv.textContent='Geolocation not supported.';errDiv.classList.remove('d-none');return;}
  btn.disabled=true;loading.classList.remove('d-none');result.classList.add('d-none');errDiv.classList.add('d-none');
  navigator.geolocation.getCurrentPosition(function(pos){
    const lat=pos.coords.latitude,lon=pos.coords.longitude;
    fetch('/api/geocode/?lat='+lat+'&lon='+lon)
      .then(r=>r.json())
      .then(d=>{
        loading.classList.add('d-none');
        if(d.error){errDiv.textContent=d.error;errDiv.classList.remove('d-none');btn.disabled=false;return;}
        document.getElementById('loc_area').textContent=d.area||'—';
        document.getElementById('loc_district').textContent=d.district||'—';
        document.getElementById('loc_state').textContent=d.state||'—';
        document.getElementById('loc_country').textContent=d.country||'India';
        if(d.state)document.getElementById('h_state').value=d.state;
        if(d.district)document.getElementById('h_district').value=d.district;
        const ss=document.querySelector('select[name="state"]');
        if(ss&&d.state){for(let o of ss.options){if(o.value===d.state){o.selected=true;break;}}}
        result.classList.remove('d-none');
        btn.innerHTML='<i class="fas fa-check-circle me-2"></i>Location Detected!';
        btn.classList.replace('btn-primary','btn-success');
        fetchWeather(lat,lon);
      })
      .catch(()=>{loading.classList.add('d-none');errDiv.textContent='Could not get location. Try again.';errDiv.classList.remove('d-none');btn.disabled=false;});
  },function(err){loading.classList.add('d-none');errDiv.textContent='Location access denied. Please allow location access in your browser.';errDiv.classList.remove('d-none');btn.disabled=false;},{timeout:10000,enableHighAccuracy:true});
}

function fetchWeather(lat,lon){
  fetch('https://wttr.in/'+lat+','+lon+'?format=j1')
    .then(r=>r.json())
    .then(d=>{
      const cur=d.current_condition?.[0];if(!cur)return;
      const temp=cur.temp_C,hum=cur.humidity;
      const tinp=document.getElementById('temperature'),hinp=document.getElementById('humidity');
      if(tinp)tinp.value=temp;if(hinp)hinp.value=hum;
      const pills=document.getElementById('weather_pills');
      if(pills)pills.innerHTML='<span class="weather-pill"><i class="fas fa-thermometer-half"></i> '+temp+'°C</span><span class="weather-pill"><i class="fas fa-tint"></i> '+hum+'%</span><span class="badge bg-success ms-2 small">Weather auto-filled ✓</span>';
    }).catch(()=>{});
}
