from django import forms
from django.shortcuts import redirect,reverse
from . import models
class SearchForm(forms.Form):

    address = forms.CharField(initial="Anywhere")
    city = forms.CharField(initial="Anywhere")
    event_type = forms.ModelChoiceField(required=False,empty_label="Any Kind", queryset=models.EventType.objects.all())
    price = forms.IntegerField(required=False)
    super_organizer = forms.BooleanField(required=False)
    

class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = [
            "name",
            "description",
            "city",
            "address", 
            "price",
            "event_date",
            "event_start",
            "event_end",
            "event_type",
            "event_rule", 
        ]
        widgets={
            'name':forms.TextInput(attrs={'placeholder':"Name of the event",'class':"myFieldclass event-name"}),
            'description':forms.Textarea(attrs={'placeholder':"Enter description for your event",'class':'myFieldClass event-description'}),
            'city':forms.TextInput(attrs={'placeholder':"Event city name",'class':"myFieldclass event-city"}),
            'address':forms.TextInput(attrs={'placeholder':"Enter address",'class':"myFieldclass event-address"}),
            'price':forms.NumberInput(attrs={'placeholder':"Price",'class':"myFieldclass event-price"}),
            'event_date':forms.DateInput(attrs={'placeholder':"Year:Month:Day",'class':"myFieldclass event-date date"}),
            'event_start':forms.TimeInput(attrs={'placeholder':"H:M:S",'class':"myFieldclass event-end-time time"}),
            'event_end':forms.TimeInput(attrs={'placeholder':"H:M:S",'class':"myFieldclass event-start-time time"}),

            # 'first_name':forms.TextInput(attrs={'placeholder':"First Name",'class':"myFieldclass name first-name"}),
            # 'last_name':forms.TextInput(attrs={'placeholder':"Last Name",'class':"myFieldclass name last-name"}),
            # 'bio':forms.Textarea( attrs={'maxlength':"20",'placeholder':"Write your bio here (Only 27 characters)",'class':"myFieldclass"}),
        }

class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = {'caption','file'}

    def save(self,pk,*args,**kwargs):
        photo = super().save(commit=False)
        event = models.Event.objects.get(pk=pk)
        photo.event = event
        photo.save()
