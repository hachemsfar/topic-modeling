from django.db import models

# Create your models here.
# myapp/models.py
class TopicInfo(models.Model):
    Topic = models.IntegerField()
    Text = models.CharField(max_length=23000)
    Name = models.CharField(max_length=255)
    Custom_Name = models.CharField(max_length=255)
    Representation = models.JSONField() 
    keyBert = models.JSONField() 
    Llama2 = models.JSONField() 
    MMR = models.JSONField() 

    def __str__(self):
        return f"Topic {self.Topic}: {self.Name}"