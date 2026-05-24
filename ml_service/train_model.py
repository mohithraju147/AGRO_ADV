"""
AGRO_ADV ML Model Trainer — XGBoost on 23 Indian Crops
Run once: python ml_service/train_model.py
"""
import numpy as np, pandas as pd, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb

CROPS = {
    'rice':        {'N':(60,120),'P':(30,60), 'K':(30,60), 'temp':(20,30),'hum':(80,90),'ph':(5.5,7.0),'rain':(1200,2200)},
    'wheat':       {'N':(80,120),'P':(40,70), 'K':(40,60), 'temp':(12,25),'hum':(50,70),'ph':(6.0,7.5),'rain':(400,800)},
    'maize':       {'N':(60,100),'P':(30,60), 'K':(20,50), 'temp':(18,30),'hum':(55,75),'ph':(5.5,7.0),'rain':(500,1000)},
    'chickpea':    {'N':(20,50), 'P':(50,80), 'K':(30,60), 'temp':(15,25),'hum':(30,60),'ph':(6.0,8.0),'rain':(300,600)},
    'kidneybeans': {'N':(15,40), 'P':(55,80), 'K':(15,40), 'temp':(16,26),'hum':(45,70),'ph':(5.5,7.0),'rain':(600,1200)},
    'pigeonpeas':  {'N':(15,40), 'P':(55,80), 'K':(15,40), 'temp':(24,35),'hum':(35,70),'ph':(5.5,7.0),'rain':(400,800)},
    'mothbeans':   {'N':(15,40), 'P':(35,60), 'K':(15,40), 'temp':(26,38),'hum':(25,55),'ph':(6.0,8.0),'rain':(200,500)},
    'mungbean':    {'N':(15,40), 'P':(35,60), 'K':(15,40), 'temp':(24,35),'hum':(55,80),'ph':(6.0,7.5),'rain':(500,900)},
    'blackgram':   {'N':(30,60), 'P':(50,80), 'K':(15,40), 'temp':(24,35),'hum':(55,80),'ph':(5.5,7.5),'rain':(600,1000)},
    'lentil':      {'N':(10,30), 'P':(55,80), 'K':(15,40), 'temp':(12,25),'hum':(35,60),'ph':(6.0,8.0),'rain':(300,600)},
    'pomegranate': {'N':(15,40), 'P':(15,40), 'K':(35,60), 'temp':(24,38),'hum':(45,70),'ph':(5.5,7.5),'rain':(400,700)},
    'banana':      {'N':(90,120),'P':(55,80), 'K':(35,60), 'temp':(24,35),'hum':(70,90),'ph':(5.5,7.0),'rain':(1200,2000)},
    'mango':       {'N':(15,40), 'P':(15,40), 'K':(35,60), 'temp':(24,35),'hum':(45,70),'ph':(5.5,7.5),'rain':(600,1200)},
    'grapes':      {'N':(15,40), 'P':(15,40), 'K':(15,40), 'temp':(18,30),'hum':(55,80),'ph':(5.5,7.0),'rain':(600,1000)},
    'watermelon':  {'N':(70,100),'P':(35,60), 'K':(35,60), 'temp':(24,35),'hum':(55,80),'ph':(5.5,7.0),'rain':(400,800)},
    'muskmelon':   {'N':(70,100),'P':(35,60), 'K':(35,60), 'temp':(24,35),'hum':(55,80),'ph':(6.0,7.5),'rain':(300,600)},
    'apple':       {'N':(15,40), 'P':(8,20),  'K':(35,60), 'temp':(8,20), 'hum':(55,80),'ph':(5.5,6.5),'rain':(800,1500)},
    'orange':      {'N':(15,40), 'P':(8,20),  'K':(8,20),  'temp':(18,30),'hum':(55,80),'ph':(5.5,7.0),'rain':(600,1200)},
    'papaya':      {'N':(40,70), 'P':(40,70), 'K':(40,70), 'temp':(24,38),'hum':(65,85),'ph':(5.5,7.0),'rain':(1000,2000)},
    'coconut':     {'N':(30,60), 'P':(15,40), 'K':(35,60), 'temp':(24,35),'hum':(65,90),'ph':(5.0,7.0),'rain':(1200,2500)},
    'cotton':      {'N':(90,120),'P':(35,60), 'K':(35,60), 'temp':(24,35),'hum':(55,80),'ph':(6.0,8.0),'rain':(600,1200)},
    'jute':        {'N':(50,80), 'P':(35,60), 'K':(35,60), 'temp':(24,38),'hum':(65,90),'ph':(6.0,7.5),'rain':(1200,2500)},
    'coffee':      {'N':(90,120),'P':(15,40), 'K':(25,50), 'temp':(18,28),'hum':(55,80),'ph':(5.5,6.5),'rain':(1500,2500)},
}

np.random.seed(42)
rows=[]
for crop,p in CROPS.items():
    for _ in range(130):
        rows.append({'N':np.random.uniform(*p['N']),'P':np.random.uniform(*p['P']),
            'K':np.random.uniform(*p['K']),'temperature':np.random.uniform(*p['temp']),
            'humidity':np.random.uniform(*p['hum']),'ph':np.random.uniform(*p['ph']),
            'rainfall':np.random.uniform(*p['rain']),'label':crop})

df=pd.DataFrame(rows)
le=LabelEncoder()
df['label_enc']=le.fit_transform(df['label'])
X=df[['N','P','K','temperature','humidity','ph','rainfall']]
y=df['label_enc']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

model=xgb.XGBClassifier(n_estimators=300,max_depth=6,learning_rate=0.1,
    subsample=0.8,colsample_bytree=0.8,use_label_encoder=False,
    eval_metric='mlogloss',random_state=42)
model.fit(X_train,y_train,eval_set=[(X_test,y_test)],verbose=False)

acc=accuracy_score(y_test,model.predict(X_test))
print(f"\nModel Accuracy: {acc:.4f} ({acc*100:.1f}%)")

os.makedirs('ml_service',exist_ok=True)
joblib.dump(model,'ml_service/crop_model.pkl')
joblib.dump(le,'ml_service/label_encoder.pkl')
print("Saved: ml_service/crop_model.pkl")
print("Saved: ml_service/label_encoder.pkl")
print(f"Crops: {list(le.classes_)}")
