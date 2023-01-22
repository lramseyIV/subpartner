from django.db import models

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.CharField(max_length=255, unique=True)
    preferred_currency = models.CharField(max_length=10)
    scammer_flag = models.CharField(max_length=5, default=0) # 0 for no 1 for yes
    scammer_count = models.IntegerField(default=0)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email} - {self.full_name} - {self.created_at}'

class Subscription(models.Model):
    subscription_name = models.CharField(max_length=255)
    cost = models.CharField(max_length=50)
    currency = models.CharField(max_length=10, default='INR')
    expiration = models.CharField(max_length=100)
    group_link = models.CharField(max_length=255)
    type = models.CharField(max_length=255) # lump sum until expiration or monthly recurring
    slots = models.IntegerField(default=0)
    slots_taken = models.IntegerField(default=0)
    slots_available = models.IntegerField(default=0)
    owner = models.ForeignKey(Customer, related_name='subscriptions_owned', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subscription_name} - {self.owner.email} - {self.created_at}'
