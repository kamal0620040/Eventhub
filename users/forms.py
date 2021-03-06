from django import forms
from django.forms import fields, widgets
from django.forms.fields import EmailField
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Email",'class':"myFieldclass"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':"myFieldclass"}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password",forms.ValidationError("Password Wrong"))
        except models.User.DoesNotExist:
            self.add_error("email",forms.ValidationError("User does not exist"))

'''
class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_re = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email="email")
            raise forms.ValidationError("User Already Exists with that Email.")
        except models.User.DoesNotExist:
            return email

    def clean_password_re(self):
        password = self.cleaned_data.get("password")
        password_re = self.cleaned_data.get("password_re")

        if password != password_re:
            raise forms.ValidationError("Password doesn't match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        #creating the user
        user = models.User.objects.create_user(email,email,password)
        user.first_name = first_name
        user.last_name =last_name
        user.save()
'''

class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name","last_name"]
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':"First Name",'class':"name first-name"}),
            'last_name':forms.TextInput(attrs={'placeholder':"Last name",'class':"name"}),
        }
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':"Email",'class':"myFieldclass"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':"myFieldclass"}))
    password_re = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Retype Password",'class':"myFieldclass"}),label="Confirm Password")

    # def clean_email(self):
    #     print("-----------------------wow----------------------------------------------")
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email="email")
    #         raise forms.ValidationError("User Already Exists with that Email.")
    #     except models.User.DoesNotExist:
    #         return email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print("----------------------------------------------------")
        print(models.User.objects.filter(email=email).exists())
        if models.User.objects.filter(email=email).exists():
            raise forms.ValidationError("User Already Exists with that Email.")
        else:
            return email

    def clean_password_re(self):
        password = self.cleaned_data.get("password")
        password_re = self.cleaned_data.get("password_re")

        if password != password_re:
            raise forms.ValidationError("Password doesn't match")
        else:
            return password

    def save(self,*args,**kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = email
        user.email = email
        user.set_password(password)
        user.save()


class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email","first_name","last_name","gender","bio","avatar"]
        widgets={
            'email':forms.TextInput(attrs={'placeholder':"Email",'class':"myFieldclass name first-name"}),
            'first_name':forms.TextInput(attrs={'placeholder':"First Name",'class':"myFieldclass name first-name"}),
            'last_name':forms.TextInput(attrs={'placeholder':"Last Name",'class':"myFieldclass name last-name"}),
            'bio':forms.Textarea( attrs={'maxlength':"20",'placeholder':"Write your bio here (Only 27 characters)",'class':"myFieldclass"}),
        }
    
