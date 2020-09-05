from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self,email,registration_no,password=None):
        if not email:
            raise ValueError('EMAIL ID IS REQUIRED')
        if not registration_no:
            raise ValueError('Registration_no ID IS REQUIRED')
        if not password:
            raise ValueError('PASSWORD IS REQUIRED')

        user=self.model(
            email=self.normalize_email(email),
            registration_no=registration_no.upper()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self,email,password,registration_no):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            registration_no=registration_no.upper()
        )

        user.is_admin=False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,registration_no):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            registration_no=registration_no.upper(),
        )

        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email                   = models.EmailField(verbose_name='email',max_length=60,unique=True)
    registration_no         = models.CharField(max_length=20,unique=True,blank=False)
    voted                   = models.BooleanField(default=False)

    date_joined             = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    #name_verified           = models.BooleanField(default=False)

    USERNAME_FIELD='registration_no'
    REQUIRED_FIELDS = ['email']
    objects=MyAccountManager()###IMPORTANT

    def __str__(self):
        return self.email

    def has_perm(self,perm,object=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class Candidate(models.Model):
    name                = models.CharField(max_length=40)
    registration_no     = models.CharField(max_length=10,unique=True)
    voter               = models.ForeignKey(User,blank=True,null=True,on_delete=models.PROTECT)
    votes               = models.IntegerField(default=0,editable=False)

    def __str__(self):
        return "{}({})".format(self.name, self.registration_no)
