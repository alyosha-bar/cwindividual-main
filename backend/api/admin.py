from django.contrib import admin
from .models import Workout, Exercise, Plan

# Register your models here.
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Plan)