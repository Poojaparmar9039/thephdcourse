from django.db import models

# Create your models here.
class user_details(models.Model):
    fullname=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField()
    status=models.CharField(max_length=20,default='Pending')
    purchase_number=models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return self.email

class order_accounts(models.Model):
    orderkey=models.CharField(max_length=50)
    email=models.EmailField()

    def __str__(self):
        return self.email