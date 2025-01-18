from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager


class User(AbstractUser):
    photo = models.ImageField(verbose_name="تصویر پروفایل", upload_to="user_images/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(null=True, blank=True, verbose_name='بیوگرافی')
    job = models.CharField(max_length=100, null=True, blank=True, verbose_name='شغل')
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True, blank=True, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post', verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('social:detail', args=[self.id])

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE, verbose_name='پست')
    image_file = models.ImageField(upload_to='post_image/', )
    title = models.CharField(max_length=200, verbose_name='عنوان', blank=True, null=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "None"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name='پست')
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    text = models.TextField(verbose_name='متن کامنت')
    active = models.BooleanField(default=False, verbose_name='وضعیت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'کامنت'
        verbose_name_plural = ' کامنت ها'

    def __str__(self):
        return f'{self.name} : {self.text}'



