from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os, uuid
from django.utils import timezone


GENDER_CHOICES = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other'),
    ('prefer_not_to_say','Prefer not to say')
)

ROLE_CHOICES = (
    ('admin','Admin'),
    ('seller','Seller'),
    ('customer','Customer')
)

def avatar_user_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'avatar', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='customer', **extra_fields):
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # role_obj, created = Role.objects.get_or_create(name=role)
        # UserRole.objects.create(user=user, role=role_obj)
        # print(f"{role_obj}")
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, role='admin', **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_role(self, role_name):
        return self.userrole_set.filter(role__name=role_name).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=avatar_user_image_file_path, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    loyalty_point = models.IntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.email}"
    


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line}, {self.city}"


class Role(models.Model):
    name = models.CharField(choices=ROLE_CHOICES, max_length=20, unique=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
