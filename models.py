from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model

LABEL_CHOICES = ((0,"Atopic Dermatitis"),(1,"Papular Urticaria"),(2,"Scabies"))

# Create your models here.
class Dataset(models.Model):
    image_path = models.URLField(max_length=200)
    def __str__(self) -> str:
        return f"{self.id}"

class Annotation(models.Model):
    image = models.ForeignKey(Dataset,on_delete=models.CASCADE)
    labeled_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    label = models.CharField(max_length=50,choices=LABEL_CHOICES)

    class Meta:
        unique_together = ('image','labeled_by')

