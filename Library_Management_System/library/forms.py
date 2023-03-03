from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .  models import *

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Book Name [ISBN]", to_field_name="isbn", label="Book (Name and ISBN)")
    name2 = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Name [Branch] [Class] [Roll No]", to_field_name="user", label="Student Details")

    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
'''
class StudentRegistration(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['branch', 'classroom_id', 'roll_no', 'phone_no']
'''
class UserExtendedForm(UserCreationForm):
    branch = forms.CharField(max_length=10, required=False)
    classroom_id = forms.CharField(max_length=10, required=False)
    roll_no = forms.CharField(max_length=8, required=False)
    phone_no = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create Student without database save")
        user = super(UserExtendedForm, self).save(commit=True)
        student = Student(user=user, branch=self.cleaned_data['branch'], classroom_id=self.cleaned_data['classroom_id'], roll_no=self.cleaned_data['roll_no'], phone_no=self.cleaned_data['phone_no'])
        student.save()
        return user, student
