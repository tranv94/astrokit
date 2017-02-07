from django.utils.http import is_safe_url
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, AuthenticationForm
from imageflow.models import UserUploadedImage



class LoginView(FormView):
    """Login using username and password
    Author: Amr Draz
    """
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = 'next'
    template_name = 'accounts/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """Logout and redirect to /
    Author: Amr Draz
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegistrationView(FormView):
    """Register using username, email, password
    Author: Amr Draz
    """
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """If the form is valid, create user and redirect to the supplied URL.
        """
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(self.request, _('Account created successfully, you can login now'))
        return super(RegistrationView, self).form_valid(form)



class MyImageList(LoginRequiredMixin, ListView):
    """Image list of authenticated user's uploaded images
    Author: Amr Draz
    """
    redirect_field_name = 'next'
    login_url = '/accounts/login/'
    model = UserUploadedImage
    paginate_by = 10

    def get_queryset(self):
        """
        Return the list of images for the current logged in user
        """
        return self.model.objects.filter(user=self.request.user).order_by('-created_at')


class BrowseImageList(ListView):
    """Image list of all uploaded images
    Author: Amr Draz
    """
    model = UserUploadedImage
    ordering = '-created_at'
    paginate_by = 1
