from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from django.utils import timezone

#send email for reset password
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  




# from phonenumber_field.modelfields import PhoneNumberField

# # Create your models here.
# SUPER_ADMIN = 'super_admin'
# STUDENT = 'student'
# VOLUNTEER = 'volunteer'
# TEACHER = 'teacher'


class User(AbstractUser):
    # ROLES = (
    #     (SUPER_ADMIN, 'Super Admin'),
    #     (STUDENT, 'Student'),
    #     (VOLUNTEER, 'Volunteer'),
    #     (TEACHER, 'Teacher'),
    # )
    username = None
    # user_type = models.CharField(max_length=25, choices=ROLES, default=SUPER_ADMIN)
    email = models.EmailField('email address', unique=True)
    sex = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_image = models.FileField(upload_to='profile', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    # contact = PhoneNumberField()
    # contact = models.BigIntegerField(null=True, blank=True, max_length=100)
    age = models.IntegerField(null=True, blank=True, max_length=50)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
