from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager


class User(AbstractUser):
    photo = models.ImageField(verbose_name="تصویر پروفایل", upload_to="user_images/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(null=True, blank=True, verbose_name='بیوگرافی')
    job = models.CharField(max_length=100, null=True, blank=True, verbose_name='شغل')
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True, blank=True, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_post', verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags=TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('social:detail', args=[self.id])
