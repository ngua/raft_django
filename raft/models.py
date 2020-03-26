from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField(
        'services.Service',
        related_name='services',
        blank=True
    )

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name}, {self.email}, {self.date})'"

    def __str__(self):
        return f'{self.name} at {self.email} on {self.date}'
