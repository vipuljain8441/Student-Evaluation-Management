from django.db import models
from django.contrib.auth.models import BaseUserManager , UserManager ,AbstractBaseUser ,AbstractUser
# Create your models here.
from .managers import CustomUserManager

#Create a model for a Roles
class customrole(models.Model):
    # name = models.CharField(max_length=20,unique=True,verbose_name = "Role",null=True,blank=True,default=None)
    name = models.CharField(max_length=20,unique=True,verbose_name = "Role",null=True,blank=True,default=None)

    def __str__(self):
        return self.name
    
#create a model for a Organisations
class Organisation(models.Model):
    name = models.CharField(max_length=50,unique=True,blank=False,null=False)
    domain = models.CharField(max_length=50)
    websiteurl = models.URLField(max_length=200,unique=True)
    orgmail =  models.EmailField(unique=True)

    def __str__(self):
        return self.name

#create a model for uploadfile
class uploadfile(models.Model):
    File = models.FileField()


# The `CustomUser` class is a model that represents a user with various fields such as name, username,
# email, phone number, role, date joined, and flags for activity, staff status, and admin status.

class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=25,blank=False,null=False)
    username = models.CharField(max_length=100, blank=True, null=False,unique=True)
    email = models.EmailField(unique=True,blank=False,null = False)
    phone_no = models.CharField(max_length=150, blank=True, null=True)
    Employee_id = models.CharField(unique=True,blank=False,default=None,null=False)
   
    role = models.ManyToManyField(customrole,blank=True)
  
    Organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    #create a instance of customusermanager to create a user
    objects = CustomUserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username','phone_no','Employee_id']
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,secustomuser):
        return True 

    def __str__(self):
        return self.username

    