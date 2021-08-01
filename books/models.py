from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=120, null=True, blank=True)

    class Meta:

      ordering = ("author",)

      def __str__(self):
        return self.title