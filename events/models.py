from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models

# Create your models here.
class AbstractType(core_models.TimeStampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class EventType(AbstractType):
    
    class Meta:
        verbose_name_plural = "Event Types"


class EventRule(AbstractType):
    
    ordering = "created"
    class Meta:
        verbose_name_plural = "Event Rules"


class Event(core_models.TimeStampedModel):

    """Event model defination"""
    name = models.CharField(max_length = 150)
    description = models.TextField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    price = models.IntegerField()
    event_date = models.DateField(null=True)
    event_start = models.TimeField()
    event_end = models.TimeField()
    organizer = models.ForeignKey(user_models.User,related_name='events',on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType,related_name='events',on_delete=models.SET_NULL,null=True)
    event_rule = models.ManyToManyField(EventRule,related_name='events',blank=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):  # intercepting the data and capitalizing the data before save it into the database
        self.city = str.capitalize(self.city)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("events:event_detail",kwargs={"pk":self.pk})

    def total_rating(self):
        all_review = self.reviews.all()
        all_rating = 0
        if len(all_review) > 0:
            for review in all_review:
                all_rating += review.rating
            return round(all_rating/len(all_review),2)
        return 0

    def first_photo(self):
        try:    
            photo, = self.photos.all()[:1]   # comma will get the first ephoto from the query set
            return photo.file.url
        except:
            pass

    def second_photo(self):
        try:
            photo, = self.photos.all()[1:2]
            return photo.file.url
        except:
            pass

    def third_photo(self):
        try:
            photo, = self.photos.all()[2:3]
            return photo.file.url
        except:
            pass


    class Meta:
        ordering = ['-created']


class Photo(core_models.TimeStampedModel):
    """ Photo Model Defination """

    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to = "event_photos")
    event = models.ForeignKey(Event,related_name="photos",on_delete=models.CASCADE)
    def __str__(self):
        return self.caption




