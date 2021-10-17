from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due' : DateInput()}
        fields = ['subject','title','description','due','is_finished']      

#common class for search form in youtube and books and disc serach 

class DashboardForm(forms.Form):
    text = forms.CharField( max_length=100,label = "Enter your serach :" )


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']


class Email(forms.EmailField): 
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. Use the 'forgot password' link on the login page")
        except User.DoesNotExist:
            return value

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        email = Email()
        fields = ['username','email','password1','password2']
        




