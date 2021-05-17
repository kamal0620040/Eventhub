from django.urls import path 
from . import views

app_name = "users"

urlpatterns = [
    path("login/",views.LoginView.as_view(),name="login"),
    path("login/github/",views.github_login,name="github-login"),
    path("login/github/callback/",views.github_callback,name="github-callback"),
    path("logout/",views.log_out,name="logout"),
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("verify/<str:key>/",views.complete_verification,name="complete-verification"),
    path("update-profile",views.UpdateProfileView.as_view(),name="update"),
    path("<int:pk>/",views.UserProfileView.as_view(),name="profile"),
]