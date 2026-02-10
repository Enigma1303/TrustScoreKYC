from django.db import models
from django.contrib.auth.models import(BaseUserManager,
                                       AbstractBaseUser, 
                                       PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_fields):
       """
       Create a normal User
       Role is Always user and cannot be overriden 
       """
       if not email:
           raise ValueError("Email is required")
       
       email=self.normalize_email(email)
       user=self.model(email=email,role=User.Role.USER,** extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user

    def create_superuser(self,email,password=None,**extra_fields):
        """
        Create system admin
        """ 
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        email=self.normalize_email(email)
        user=self.model(email=email,role=User.Role.ADMIN,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    email=models.EmailField(unique=True)
    role= models.CharField(max_length=10,choices=Role.choices,default=Role.USER)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)


    objects=UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email







