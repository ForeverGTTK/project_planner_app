from xml.parsers.expat import model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid



class Projects(models.Model):

    
    project_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    project_name = models.TextField(null=True,blank=True)
    owner_ID = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    public =  models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated =  models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.project_name

class data_container(models.Model):
    
    container_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    project_ID = models.ForeignKey(Projects , on_delete=models.CASCADE, null=True)
    container_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    last_updated =  models.DateTimeField(auto_now=True,)
    

class data_items(models.Model):
    
    item_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    container = models.ForeignKey(data_container , on_delete=models.CASCADE, null=True)
    container_rel = models.ManyToOneRel(container,data_container,item_ID)
    item_name = models.TextField(null=True)
    item_description = models.TextField(null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    last_updated =  models.DateTimeField(auto_now=True)
    
    
class container_relation(models.Model):
    
    relation_ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(data_container , on_delete=models.SET_NULL, null=True ,related_name='sender')
    receiver = models.ForeignKey(data_container , on_delete=models.SET_NULL, null=True, related_name='reciever')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    last_updated =  models.DateTimeField(auto_now=True)
    



    def __str__(self) -> str:
        text = f'from {self.sender} to {self.reciver}'
        return text
    

