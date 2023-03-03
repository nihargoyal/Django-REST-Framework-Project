from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

app_name='library'

urlpatterns = [
    path("", views.index, name="library"),
    path("add_book/", staff_member_required(views.BookCreate.as_view()), name="add_book"),
    path("view_books/", views.BookList.as_view(), name="view_books"),
    path("view_students/", staff_member_required(views.StudentList.as_view()), name="view_students"),
    #path("issue_book/<int:pk>", staff_member_required(views.BookInstanceUpdate.as_view()), name="issue_book"),
    #path("view_issued_book/", staff_member_required(views.IssuedBookList.as_view()), name="view_issued_book"),
    #path("student_issued_books/", views.StudentIssuedBooks.as_view(), name="student_issued_books"),
    path("issue_book/", staff_member_required(views.issue_book), name="issue_book"),
    path("view_issued_book/",  staff_member_required(views.view_issued_book), name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.user_profile, name="profile"),
    path("edit_profile/<int:pk>/", views.StudentUpdate.as_view(), name="edit_profile"),
    path("student_registration/", views.StudentCreate.as_view(), name="student_registration"),
    path("change_password/", views.ChangePassword.as_view(), name="change_password"),
    path("student_login/", views.Login.as_view(), name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("delete_book/<int:pk>/", staff_member_required(views.BookDelete.as_view()), name="delete_book"),
    #path("delete_issue/<int:myid>/", staff_member_required(views.IssueDelete.as_view()), name="delete_issue"),
    path("view_book/<int:pk>/", views.BookDetail.as_view(), name="view_book"),
    path("delete_student/<int:pk>/", staff_member_required(views.StudentDelete.as_view()), name="delete_student"),
]