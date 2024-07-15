from xml.parsers.expat import model
from django.db import models


class Projects(models.Model):
    #host
    #topic
    project_name = models.TextField(null=True,blank=True)
    public =  models.BinaryField()
    creation = models.DateTimeField(auto_now_add=True)
    last_updated =  models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.project_name} created in {self.creation}, last updated {self.last_updated}'
