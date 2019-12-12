from django.db import models
from django.utils import timezone
from base.models import BaseModel
from django.urls import reverse
from PIL import Image


class User(BaseModel):
    ROLE = (
        ('admin', 'admin'),
        ('staff', 'staff'),
        ('moderator', 'moderator'),
        ('other', 'other')
    )
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=15, blank=False, unique=True)
    phone2 = models.CharField(max_length=15, blank=True, unique=True)
    email = models.EmailField(max_length=70, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(choices=ROLE, blank=False, max_length=10)
    date_joined = models.DateTimeField(auto_now_add= True)
    profile_pic = models.ImageField(upload_to='profile_pics')
    bio = models.TextField(max_length=60, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    class Meta:
        abstract = True


class Address(models.Model):
    Country = (
        ('USA', 'USA'),
        ('China', 'China'),
        ('Russia', 'Russia'),
        ('China', 'China'),
        ('India', 'India'),
        ('Nepal', 'Nepal')
    )

    country = models.CharField(choices=Country, default='Nepal', max_length=10)
    city = models.CharField(max_length=20, blank=False)
    postcode = models.CharField(max_length=10, blank=True)

    class Meta:
        abstract = True


class Account(User, Address):
    STATUS = (
        ('open',  'open'),
        ('close', 'close')
    )
    username = models.CharField(max_length=25, unique=True, blank=False)
    account_name = models.CharField(max_length=20, blank=False)
    created_by = models.CharField(max_length=20)
    status = models.CharField(choices=STATUS, max_length=10)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "User_Account"


class Task(models.Model):
    WORK_STATUS = (
        ('New', 'New'),
        ('In_Progress', 'In_Progress'),
        ('Completed', 'Completed')
    )
    WORK_PRIORITY = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )
    title = models.TextField(max_length=50, blank=False)
    status_choice = models.TextField(max_length=15, choices=WORK_STATUS, blank=True)
    priority_choice = models.TextField(max_length=15, choices=WORK_PRIORITY)
    created_by = models.CharField(max_length=15, blank=False)
    assigned_to = models.ForeignKey(Account, blank=False, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(timezone.now)

    def __str__(self):
        return self.priority_choice


class Comment(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    comment = models.TextField(max_length=120, blank=True)
    commented_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    commented_on = models.DateTimeField(timezone.now)


class Notice(models.Model):
    notice1 = models.TextField(max_length=200, blank=True)
    notice2 = models.TextField(max_length=200, blank=True)
    posted_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notice'
