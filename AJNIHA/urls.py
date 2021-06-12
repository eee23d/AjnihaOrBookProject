from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('loginPage',views.loginPage,name='loginPage'),
    path('logoutUser',views.logoutUser,name='logoutUser'),
    path('setting', views.setting, name='setting'),
    path('myNotes', views.myNotes, name='myNotes'),
    path('allNotes',views.allNotes,name='allNotes'),
    path('liked', views.liked, name='liked'),
    path('contact',views.contact,name='contact'),
    path('library',views.library,name='library'),
    path('search',views.search,name='search'),
    path('stat',views.stat,name='stat'),
    path('suggest',views.suggest, name='suggest'),
    path('contactUs',views.contactUs, name='contactUs'),
    path('thanks', views.thanks, name='thanks'),

]