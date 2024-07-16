from xml.parsers.expat import model
from django.contrib.auth.models import User
from django.db import models
import uuid



class Projects(models.Model):
    #host
    #topic
    
    projectID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    project_name = models.TextField(null=True,blank=True)
    owner_id = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    public =  models.BinaryField()
    creation = models.DateTimeField(auto_now_add=True)
    last_updated =  models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'<li><strong>{self.project_name}</strong>    created in {self.creation.date()}     last updated {self.last_updated.date()}</li>'

class data_container(models.Model):
    
    container_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    projectID = models.ForeignKey(Projects , on_delete=models.CASCADE, null=True)
    itemx = models.IntegerField()
    itemy = models.IntegerField()

class data_items(models.Model):
    
    item_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    item_name = models.ForeignKey(data_container , on_delete=models.CASCADE, null=True)
    item_description = models.TextField()
    message = models.CharField(max_length=255)
    
class container_relation(models.Model):
    
    relation_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(data_container , on_delete=models.SET_NULL, null=True ,related_name='sender')
    receiver = models.ForeignKey(data_container , on_delete=models.SET_NULL, null=True, related_name='reciever')



    def __str__(self) -> str:
        text = f'from {self.sender} to {self.reciver}'
        return text
    

