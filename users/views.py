import os
from django.forms import widgets
from django.views.generic.edit import UpdateView
import requests
from users import models
from django.contrib import auth
from django.http.response import HttpResponseRedirectBase
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView,DetailView,UpdateView
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms,mixins
import users

# Create your views here.
'''
class LoginView(View):

    def get(self,request):
        form = forms.LoginForm()
        return render(request,"users/login.html",{"form":form})

    def post(self,request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=email,password=password)
            if user is not None:
                login(request,user)
                return redirect(reverse("core:event"))

        return render(request,"users/login.html",{"form":form})
'''

# implementing using form view

class LoginView(mixins.LoggedOutOnlyView,FormView):
    
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:event")

    def form_valid(self,form):
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request,username=email,password=password)
            if user is not None:
                login(self.request,user)
                messages.success(self.request,f"Welcome Back, {user.first_name}")
                return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:event")

def log_out(request):
    messages.info(request,f"See you later")
    logout(request)
    return redirect(reverse("core:home"))
 
 
class SignUpView(mixins.LoggedOutOnlyView,FormView):
    
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:event")

    def form_valid(self,form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request,username=email,password=password)
        if user is not None:
            login(self.request,user)
        
        # user.verify_email()
        # messages.success(self.request,"Verification link sent to your mail.")
        messages.success(self.request,"Verification is turned off.")
        return super().form_valid(form)
    
def complete_verification(request,key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # success message here
    except models.User.DoesNotExist:
        # failed message here
        pass
    messages.success(request,"Email Verified")
    return redirect(reverse("core:event"))
    


def github_login(self):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user,user:email")

class GithubException(Exception):
    pass

def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code","None")
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = token_request.json()
            error = result_json.get("error",None)
            if error is not None:
                return GithubException("Can't get the access token")
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_request = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_json = email_request.json()
                profile_json = profile_request.json()
                # print(profile_json)
                username = profile_json.get("login",None)
                if username is not None:
                    name = profile_json.get("name")
                    email = email_json[0].get("email")
                    # user = models.User.objects.get(email=email)
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException (
                                f"Please login with:{user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(username=email,first_name=name,email=email,login_method = models.User.LOGIN_GITHUB,email_verified=True,)
                        user.set_unusable_password()
                        user.save()
                    login(request,user)
                    messages.success(request,f"Welcome Back, {user.first_name}")
                    return redirect(reverse("core:event"))

                    
                    # if user is not None:
                    #     return redirect(reverse("users:login"))
                    # else:
                    #     user = models.User.objects.create(username=email,first_name=name,email=email)
                    #     login(request,user)
                    #     return redirect(reverse("core:event"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as err:
        messages.error(request,err)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User    
    context_object_name = "user_obj"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

class UpdateProfileView(mixins.EmailLoginOnlyView,mixins.LogInOnlyView,UpdateView):

    model = models.User
    form_class = forms.UpdateForm
    template_name = "users/update-profile.html"
    context_object_name = "user_edit"
    # fields = {
    #     "first_name",
    #     "last_name",
    #     "avatar",
    #     "gender",
    #     "bio",    
    # }
    
    def get_object(self,queryset=None):
        return self.request.user


    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if email != "":
            print("yo runvayo")
            self.object.username = email
        self.object.save()
        messages.success(self.request,"Profile updated")
        return super().form_valid(form)


class UpdatePasswordView(mixins.LogInOnlyView,SuccessMessageMixin,PasswordChangeView):
    
    template_name= "users/update-password.html"
    success_message = "Password Updated"
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"class":"myFieldclass"}
        form.fields["new_password1"].widget.attrs = {"class":"myFieldclass","onfocus":"closeye()"}
        form.fields["new_password2"].widget.attrs = {"class":"myFieldclass","onfocus":"closeye()"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()