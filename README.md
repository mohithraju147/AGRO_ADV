# 🌱 AGRO_ADV — AI Smart Farming Advisor

Full-stack Django + XGBoost ML crop recommendation system for Indian farmers.

## Quick Start (Run these 6 commands)

```bash
# 1. Enter project folder
cd agro_adv

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database + load sample data
python manage.py makemigrations farmers crops market predictions schemes
python manage.py migrate
python manage.py seed_data

# 5. Train the AI model (takes ~30 seconds)
python ml_service/train_model.py

# 6. Create admin + run server
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000

## All URLs
| Page | URL |
|---|---|
| Home | http://127.0.0.1:8000/ |
| Predict Crop | http://127.0.0.1:8000/predict/ |
| Results | http://127.0.0.1:8000/results/ |
| Market Prices | http://127.0.0.1:8000/market/ |
| Encyclopedia | http://127.0.0.1:8000/encyclopedia/ |
| Govt Schemes | http://127.0.0.1:8000/schemes/ |
| Profile | http://127.0.0.1:8000/profile/ |
| History | http://127.0.0.1:8000/history/ |
| Django Admin | http://127.0.0.1:8000/admin/ |
| REST API | http://127.0.0.1:8000/api/ |

## Features
- XGBoost ML model — 23 Indian crops, 7 inputs (N, P, K, pH, temp, humidity, rainfall)
- Live location detection using OpenStreetMap (no API key needed)
- Weather auto-fill from wttr.in (no API key needed)
- 40+ market prices from APMC markets across India
- Government schemes linked to predicted crop on results page
- Nearby market prices filtered by detected state
- 6-language support: English, Kannada, Hindi, Telugu, Tamil, Marathi
- Full prediction history per farmer
- Django Admin panel for all data management
- REST API at /api/ for all models
