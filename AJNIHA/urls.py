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
    path('userHome',views.userHome,name='userHome'),
    path('notes',views.notes,name='notes'),
    path('contact',views.contact,name='contact'),
    path('library',views.library,name='library'),
    path('search',views.search,name='search'),
    path('stat',views.stat,name='stat'),

    #I add a comment here to try use commit why

]