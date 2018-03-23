from __future__ import unicode_literals
from django.db import models

class QuoteManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors["quoted_by"] = "Quoted by should be more than 3 characters"
            
        if len(postData['message']) < 10:
            errors["message"] = "Message should be more than 10 characters"
        return errors


class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    poster = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name="posted_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuoteManager()

# Many to many relationship between users and quotes
class Favorite(models.Model):
    # One user can have many favorite quotes
    user = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name="user_favorites")
    # One quote can be loved by many users
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="quote_favorites")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)