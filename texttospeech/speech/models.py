from django.db import models

class MyFileModel(models.Model):
    file = models.FileField(upload_to='uploads/')
    email_address = models.EmailField(default='default@example.com')

    def __str__(self):
        return self.email_address
