from django.urls import path,include
from .views import index,details,poll

app_name='poll'

urlpatterns=[
    path('',index,name='polls-list'),
    path('<int:id>/details',details,name='polls-details'),
    path('<int:id>/',poll,name='single_poll'),
]