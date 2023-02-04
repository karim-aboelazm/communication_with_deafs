from django.db import models

class SignToTextImage(models.Model):
    image = models.ImageField(upload_to="signs/")
    def __str__(self):
        return f"image : {self.id}"