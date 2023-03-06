from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    timezone = models.CharField(max_length=50, default='-03:00')
    language = models.CharField(max_length=2, choices=(('pt', 'Português'), ('es', 'Espanhol'), ('en', 'Inglês')), default='pt')
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_companies')
    invited_users = models.ManyToManyField('User', related_name='companies_invited')
    
class Document(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    sign_deadline = models.DateTimeField()
    is_signed = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='documents')
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_documents')
    
class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    last_password_reset = models.DateTimeField(default=timezone.now)
    is_email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    original_company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, related_name='users')
    companies = models.ManyToManyField('Company', related_name='users')
    documents = models.ManyToManyField('Document', related_name='users')


class Company(models.Model):
    LANGUAGES = (
        ('pt', 'Português'),
        ('es', 'Espanhol'),
        ('en', 'Inglês'),
    )

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=50, default='-03:00')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='pt')
    invited_users = models.ManyToManyField(User, related_name='invited_companies')
    owner = models.ForeignKey(User, related_name='owned_companies', on_delete=models.CASCADE)
    documents = models.ManyToManyField('Doc', related_name='companies')

    def __str__(self):
        return self.name
