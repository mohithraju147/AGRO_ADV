from django.urls import path
from . import views
urlpatterns = [
    path('',              views.home,           name='home'),
    path('login/',        views.login_page,     name='login'),
    path('login/verify/', views.login_verify,   name='login_verify'),
    path('logout/',       views.logout_view,    name='logout'),
    path('profile/',      views.farmer_profile, name='farmer_profile'),
    path('predict/',      views.predict,        name='predict'),
    path('results/',      views.results,        name='results'),
    path('market/',       views.market,         name='market'),
    path('encyclopedia/', views.encyclopedia,   name='encyclopedia'),
    path('schemes/',      views.schemes,        name='schemes'),
    path('history/',      views.history,        name='history'),
    path('api/geocode/',  views.geocode_api,    name='geocode_api'),
]
