from email.policy import default
from xml.parsers.expat import model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    
    ID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        

class Projects(BaseModel):

    
    name = models.TextField(null=False,blank=False)
    owner_ID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_projects')
    is_public =  models.BooleanField(default = True)
    
    
    def __str__(self) -> str:
        return f'<strong>{self.name}</strong>  {self.description}'

class data_container(BaseModel):
    
    project_ID = models.ForeignKey(Projects , on_delete=models.CASCADE, null=True)
    is_root =  models.BooleanField(default = True)
    level = models.IntegerField()
    prequisit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='required_by')
   
    def get_children(self):
        return data_container.objects.filter(parent_relations__parent=self)

    def get_data(self):
        return data_items.objects.filter(container = self)
    
    def clean(self):
    # Ensure that 'prequisit' is set if 'is_root' is False
        if not self.is_root and not self.prequisit:
            raise ValidationError({
                'prequisit': 'Prequisit must be set for non-root containers.'
            })
    
    def __str__(self) -> str:
        return f'{self.get_data()}'

class data_items(BaseModel):
    
    container = models.ForeignKey(data_container , on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)
    message = models.CharField(max_length=255)
   
    def __str__(self) -> str:
        return self.message
    
    
class container_relation(BaseModel):
    
   project_ID = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
   parent = models.ForeignKey(data_container, on_delete=models.SET_NULL, null=True, related_name='parent_relations')
   child = models.ForeignKey(data_container, on_delete=models.SET_NULL, null=True, related_name='child_relations')
  



   def __str__(self) -> str:
        text = f'from {self.parent} to {self.child}'
        return text
    

