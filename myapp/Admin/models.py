from django.db import models


class user_details(models.Model):
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField() 
    status = models.CharField(max_length=20, default='Pending')
    purchase_number = models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

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

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# ✅ Tracks if a specific user has completed a specific module
class UserProgress(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.module.title} - {'Done' if self.completed else 'Pending'}"
