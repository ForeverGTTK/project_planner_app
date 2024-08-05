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
    
    class Meta:
        ordering = ['created_at']
    

    def build_dep_tree(self):
        """
        Builds a dependency tree for the project.
        Returns a dictionary representing the hierarchical structure:
        {
            "[root_1_ID]": {
                "[lvl1_child_1_ID]": {
                    "[lvl_n_child_1_ID]": {...},
                    "[lvl_n_child_n_ID]": {...},
                },
                "[lvl1_child_2_ID]": {...},
                ...
            },
            "[root_2_ID]": {...},
            ...
        }
        """
        root_containers = data_container.objects.filter(project_ID=self, is_root=True)
        tree = {}
        containers = {}

        for root in root_containers:
            tree[root] = self.build_sub_tree(root)
    
        return tree

    def build_sub_tree(self, container):
        sub_tree = {}
        children = container.child_relations.all()
        for child_relation in children:
            child = child_relation.child
            sub_tree[child] = self.build_sub_tree(child)
        return sub_tree



    def get_project(self):
        containers = data_container.objects.filter(project_ID = self)
        relations = container_relation.get_project_relations(self)
        return {
            'containers': containers,
            'relations': relations,
            }

    def __str__(self) -> str:
        return f'{self.name} - {self.description}'

class data_container(BaseModel):
    
    project_ID = models.ForeignKey(Projects , on_delete=models.CASCADE, null=True)
    is_root =  models.BooleanField(default = True)
    level = models.IntegerField()
    prequisit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True, related_name='required_by')
    
    class Meta:
        ordering = ['level','created_at']

    def get_children(self):
        return data_container.objects.filter(parent_relations__parent=self)

    def get_child_count(self):
        return self.get.count()
    
    def get_data(self):
        items= data_items.objects.filter(container = self)
        items_as_list = []
        for item in items:
            items_as_list.append(item.message)
        return items_as_list
    
    
    
    def __str__(self) -> str:
        return f'{self.description} (container level {self.level})'

class data_items(BaseModel):
    
    container = models.ForeignKey(data_container , on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)
    message = models.CharField(max_length=255)
   
    def __str__(self) -> str:
        return f'{self.message}'
    
    
class container_relation(BaseModel):
    
   project_ID = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
   parent = models.ForeignKey(data_container, on_delete=models.CASCADE, null=True, related_name='child_relations')
   child = models.ForeignKey(data_container, on_delete=models.CASCADE, null=True, related_name='parent_relations')
  
   @staticmethod
   def get_project_relations(project_ID):
       relations = container_relation.objects.filter(project_ID=project_ID)
       return relations

   @staticmethod
   def build_tree(container, tree, level=0):
       if level not in tree:
           tree[level] = 0
       tree[level] += 1
        
       children = container.child_relations.all()
       for child_relation in children:
           container_relation.build_tree(child_relation.child, tree, level + 1)

   def __str__(self) -> str:
        text = f'from {self.parent} to {self.child}'
        return text

