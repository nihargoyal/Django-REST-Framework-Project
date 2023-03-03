from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'genre', 'language']

admin.site.register(Book, BookAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'branch', 'classroom_id', 'roll_no', 'phone_no']

admin.site.register(Student, StudentAdmin)

class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'isbn', 'issued_date', 'expiry_date']

admin.site.register(IssuedBook, IssuedBookAdmin)

'''
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'imprint', 'status', 'borrower', 'issued_date', 'expiry_date']

admin.site.register(BookInstance, BookInstanceAdmin)'''