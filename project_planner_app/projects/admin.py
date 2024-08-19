from django.contrib import admin

from .models import *

models= [Projects,data_container,data_items,container_relation,Topics,topic_relations]
for model in models:
    admin.site.register(model)

# Register your models here.
