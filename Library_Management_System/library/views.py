from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponse, redirect
from . models import *
from . forms import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from library.forms import IssueBookForm
from . import forms, models
from .forms import IssueBookForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

def index(request):
    return render(request, "homepage.html")

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'add_book.html'
    success_url="/view_books"

class BookList(LoginRequiredMixin, ListView):
    model = Book
    fields = '__all__'
    template_name = 'view_books.html'

class BookDetail(LoginRequiredMixin,DetailView):
    model=Book
    fields='__all__'
    template_name = 'view_book.html'

class StudentList(LoginRequiredMixin, ListView):
    model = Student
    fields = '__all__'
    template_name = 'view_students.html'

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = IssueBookForm
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            obj = IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        i=0
        for l in books:
            t=(students[i].user,students[i].user_id,books[i].title,books[i].isbn,issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.title,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})


'''
class BookInstanceUpdate(LoginRequiredMixin, UpdateView):
    model = BookInstance
    fields = '__all__'
    template_name = 'issue_book.html'

class IssuedBookList(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'view_issued_book.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status='o').all()

class StudentIssuedBooks(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'student_issued_books.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user.id).all()
'''

@login_required(login_url = '/student_login')
def user_profile(request):
    return render(request, "profile.html")


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = UserExtendedForm
    template_name = 'edit_profile.html'
    success_url="/profile"

class BookDelete(LoginRequiredMixin, DeleteView):
    model=Book
    template_name = 'book_confirm_delete.html'
    success_url="/view_books"

class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = "/view_students"

class StudentCreate(CreateView):
    form_class=UserExtendedForm
    template_name='student_registration.html'

    def get_success_url(self):
        return reverse_lazy("library:student_login")

class Login(LoginView):
    template_name = 'student_login.html'

class Logout(LogoutView):
    template_name = 'logout.html'
    success_url = "/"

class ChangePassword(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = "/profile"

#class ChangePasswordDone(PasswordChangeDoneView):
#    template_name = 'change'

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")
