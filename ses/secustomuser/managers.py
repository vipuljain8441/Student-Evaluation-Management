from django.contrib.auth.models import BaseUserManager , UserManager ,AbstractBaseUser ,AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
# CustomUser = get_user_model()


#create a customusermanager for a create user and create superuser
class CustomUserManager(BaseUserManager):
    use_in_migrations= True
   
    def create_user(self,email,username,name,password,**extra_fields):
        if not email:
            raise ValueError("The Email Field must be Set!")
        email = self.normalize_email(email)
        user  = self.model(email=email,username = username,name = name,**extra_fields)
        user.set_password(password)
        user.save(using =self.db)
        return user
    
    def create_superuser(self,email,username,name,password ,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        # extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, username, name, password, **extra_fields)

    