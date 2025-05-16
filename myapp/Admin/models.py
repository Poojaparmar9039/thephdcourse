from django.db import models
from datetime import datetime
from django.utils.timezone import now


class user_details(models.Model):
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField() 
    status = models.CharField(max_length=20, default='Pending')
    purchase_number = models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    orderkey=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.fullname} ({self.email})"


class order_accounts(models.Model):
    orderkey = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} - {self.orderkey}"


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    def total_modules(self):
        return self.module_set.count()  


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

from django.utils import timezone

class UserProgress(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.FloatField(default=0.0)
    last_accessed_on = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.email} - {self.module.title} - {'Completed' if self.completed else 'Pending'} - {self.progress_percentage}%"




class Certificate(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # Assuming you have a Course model
    generated_on = models.DateTimeField(default=timezone.now)
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Certificate for {self.user.email} - {self.course.name}"
