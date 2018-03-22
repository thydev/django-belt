from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
import re


# create a regular expression object that we can use run operations on
email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
pwd_reg = re.compile('^(?=\S{8,30}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

# No methods in our new manager should ever catch the whole request object with a parameter!!! 
# (just parts, like request.POST)
class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"
        
        email = postData['email']
        if not email_reg.match(email):
            errors['email'] = "Invalid email address"
        elif User.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "This email {} is already exist".format(postData['email'])

        password = postData['password']
        password_confirm = postData['password_confirm']
        if (len(password) < 0):
            errors['password'] = "Please input your password"
        elif not pwd_reg.match(password):
            errors['password'] = "Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 symbol"
        elif password != password_confirm:
            errors['password'] = "Password does not match!"

        return errors

    def update_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"
        if not email_reg.match(email):
            errors['email'] = "Invalid email address"
        # Check the email if it already exists and do not count its self
        # print "user filter", User.objects.exclude(id = postData['user_id']).filter(email = postData['email']).count()
        # print User.objects.filter(~Q(id = postData['user_id']) & Q(email = postData['email'])).count()
        elif User.objects.filter(~Q(id = postData['user_id']) & Q(email = postData['email'])).count() > 0:
            errors['email'] = "This email {} already exists".format(postData['email'])

        if (len(password) < 0):
            errors['password'] = "Please input your password"
        elif not pwd_reg.match(password):
            errors['password'] = "Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 symbol"
        elif password != password_confirm:
            errors['password'] = "Password does not match!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    date_birth = models.DateField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties !
    objects = UserManager()

    def __repr__(self):
        return "<User:{} {}>".format(self.first_name, self.last_name)

# class Book_review(models.Model):
#     # One user can review many books
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_books")
#     # One book can be reviewed by many users
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviewed_by_users")
#     review = models.TextField()
#     rating = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    