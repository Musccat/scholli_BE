from django.contrib import admin
from .models import Profile, Wishlist, UserSubscription

# Profile 모델 
admin.site.register(Profile)

# Wishlist 모델
admin.site.register(Wishlist)

# 구독 모델
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'expiration_date')
    list_filter = ('is_active',)
