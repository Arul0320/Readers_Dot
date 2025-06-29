from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label='Enter OTP')

class ParagraphForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=50, label='What was the last word you read?')

class StudentInfoForm(forms.Form):
    student_name = forms.CharField(max_length=100, label='Your Name')   