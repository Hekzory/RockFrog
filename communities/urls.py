from django.urls import path
from .views import *


app_name = 'communities'

urlpatterns = [
    path('', home, name='home'),
    path('create/', creategroup, name='creategroup'),   
    path('<str:groupslug>/', community, name='community'),
    path('<str:groupslug>/collection/', collection, name='collection'),
    path('<str:groupslug>/information/', information, name='information'),
    path('<str:groupslug>/edit/', editgroup, name='editgroup'),
    path('<int:groupid>/collection/addtocollection/', AddToCollection.as_view(), name='addtocollection'),
    path('<int:groupid>/moreedit/', edit, name='edit'),
    path('<int:groupid>/edit/moreedit/', moreedit, name='moreedit'),
    path('<int:groupid>/subscribe/', subscribe, name='subscribe'),
    path('<int:groupid>/unsubscribe/', unsubscribe, name='unsubscribe')
]