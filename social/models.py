from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(verbose_name="تصویر پروفایل", upload_to="user_images/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(null=True, blank=True, verbose_name='بیوگرافی')
    job = models.CharField(max_length=100, null=True, blank=True, verbose_name='شغل')
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True, blank=True)
