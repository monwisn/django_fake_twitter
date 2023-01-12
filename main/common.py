from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


class UserAccessMixin(PermissionRequiredMixin):
    # We're adding items to the dispatch to be performed by the view
    # dispatch() method takes in the request from the user and ultimately then returns a response
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/books/')

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)