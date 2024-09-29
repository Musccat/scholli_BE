from django.contrib import admin
from .models import Profile, Wishlist

# Profile 모델 
admin.site.register(Profile)

# Wishlist 모델
admin.site.register(Wishlist)
