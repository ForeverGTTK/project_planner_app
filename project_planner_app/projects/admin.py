from django.contrib import admin

from .models import Projects,data_container,data_items,container_relation

models= [Projects,data_container,data_items,container_relation]
for model in models:
    admin.site.register(model)

# Register your models here.
