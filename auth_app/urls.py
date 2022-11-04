from django.urls import path 
from .views import *

urlpatterns = [ 
    path('entrar/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registrar/', Registrar.as_view(), name='registrar')
]