from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def set_password(self,raw_password):
        self.password=make_password(raw_password)
    
    def check_password(self,raw_password):
        return check_password(raw_password,self.password)
    
    @property
    def is_authenticated(self):
        return True

class EmailSettings(models.Model):
    smtp_server=models.CharField(max_length=100, default="default_smtp_server")
    port=models.IntegerField()  
    use_tls=models.BooleanField(default=True)  
    username=models.CharField(max_length=100)  
    password=models.CharField(max_length=128, default="default_password")

    def __str__(self):
        return self.username

class PasswordReset(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id=models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    created_when=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.user.name} at {self.created_when}"

class UserMetrics(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    rank=models.IntegerField(default=0)
    rating=models.IntegerField(default=0)
    total_hours=models.IntegerField(default=0)

class UserAchievements(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bronze_badges=models.IntegerField(default=0)
    silver_badges=models.IntegerField(default=0)
    gold_badges=models.IntegerField(default=0)

class UserData(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    hours=models.IntegerField()
    