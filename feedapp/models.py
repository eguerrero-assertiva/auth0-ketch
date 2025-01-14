from django.db import models

# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.FileField(upload_to="images/", blank=True)

    def __str__(self):
        return "{}:{}..".format(self.id, self.title[:10])