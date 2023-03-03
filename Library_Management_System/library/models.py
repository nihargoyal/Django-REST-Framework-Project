from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=10)
    classroom_id = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=8)
    phone_no = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom_id)+']' + " ["+str(self.roll_no)+']'
'''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.student.save()
'''
def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
'''
class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)

    loan_status = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1, choices=loan_status, blank=True, default='m')
    borrower = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    issued_date = models.DateField(blank=True)
    expiry_date = models.DateField(blank=True)

#    class Meta:
#        ordering = ['due_back']

    def __str__(self):
        return f"{self.id}-->{self.book.title}"
'''