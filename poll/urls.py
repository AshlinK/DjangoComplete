from django.urls import path,include
from .views import index,details,poll,PollView

app_name='poll'

urlpatterns=[
    path('add/',PollView.as_view(),name='poll_add'),
    path('<int:id>/edit/',PollView.as_view(),name='poll_edit'),
    path('<int:id>/delete/',PollView.as_view(),name='poll_delete'),
    path('add/',PollView.as_view(),name='poll_add'),
    path('',index,name='polls-list'),
    path('<int:id>/details',details,name='polls-details'),
    path('<int:id>/',poll,name='single_poll'),
]