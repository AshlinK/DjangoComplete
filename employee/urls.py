from django.urls import re_path,include
from .views import employee_list,employee_details,employee_add,employee_edit,employee_delete

app_name='employee'

urlpatterns=[
    re_path(r'^$',employee_list,name='emp_list'),
    re_path(r'^details/<int:id>/$',employee_details,name='emp_details'),
    re_path(r'^add/$',employee_add,name='emp_add'),
    re_path(r'^edit/(?P<id>\d+)/$',employee_edit,name='emp_edit'),
    re_path(r'^delete/(?P<id>\d+)/$',employee_delete,name='emp_delete'),
]