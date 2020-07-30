from .models import User
from django.contrib.auth.models import Group

class RoleMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        # One time configuration and initialization

    def __call__(self,request):
        """
        Code to be executed for each request before the view,
        (and other middlewares) are called.
        """

        response=self.get_response(request)
        """
        Code to be executed for each request/response after the view
        is called.
        """

        return response

    def process_view(self,request,view_func,*view_args,**view_kwargs):
        """
        Called just before Django calls the view. Returns either an
        HttpResponse or None.
        """
        if request.user.is_authenticated:
            request.role=None
            groups=request.user.groups.all()
            if groups:
                request.role=groups[0].name
            else:
                group=Group.objects.all()
                request.user.groups.add(group[0])            
                request.role=group[0].name
                