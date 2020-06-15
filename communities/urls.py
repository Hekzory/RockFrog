from django.urls import path
from .views import *
from django.conf import settings

app_name = 'communities'

urlpatterns = [
    path('', home, name='home'),
    path('create/', creategroup, name='creategroup'),   
    path('<str:groupslug>/', community, name='community'),
    path('<str:groupslug>/collection/', collection, name='collection'),
    path('<str:groupslug>/information/', information, name='information'),
    path('<str:groupslug>/edit/', editgroup, name='editgroup'),

    path('<int:groupid>/createarticle/', CreateArticle.as_view(), name='createarticle'),
    path('<int:groupid>/editarticle/<int:articleid>/', EditArticle.as_view(), name='editarticle'),
    path('<int:groupid>/collection/addtocollection/', AddToCollection.as_view(), name='addtocollection'),
    path('<int:groupid>/deletearticle/<int:articleid>/', DeleteArticle.as_view(), name='deletearticle'),
    path('<int:groupid>/moreedit/', edit, name='edit'),    
    path('<int:groupid>/edit/moreedit/', moreedit, name='moreedit'),
    path('<int:groupid>/subscribe/', subscribe, name='subscribe'),
    path('<int:groupid>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('<int:groupid>/like/<str:articleid>/', like, name='like'),  
    path('<int:groupid>/removelike/<str:articleid>/', removelike, name='removelike'),  
]