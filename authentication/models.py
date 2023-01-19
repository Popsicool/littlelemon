from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password, username, phone_num, **extra_fields):
        if not email:
            raise valueerror("Email must be provided")
        if not password:
            raise valueerror("Password must be provided")

        user = self.model(
            email  = self.normalize_email(email),
            username = username,
            phone_num = phone_num,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, username,phone_num, **extra_fields):
        return self._create_user(email, password,username,  phone_num)

    def create_superuser(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password,username=None,  phone_num=None, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    email= models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=240, null=True)
    phone_num = models.CharField(max_length=50, null=True)
    is_staff = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_superuser =  models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username