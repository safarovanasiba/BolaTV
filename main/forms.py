from django import forms
from django.contrib.auth.hashers import make_password
from .models import Ariza, TestQuestion, Users

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Foydalanuvchi nomi", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parol", "class": "form-control"})
    )

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parolni tasdiqlang", "class": "form-control"})
    )
    
    class Meta:
        model = Users
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Foydalanuvchi nomi", "class": "form-control"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Parol", "class": "form-control"}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Parollar mos kelmadi")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ArizaForm(forms.ModelForm):
    class Meta:
        model = Ariza
        fields = ["full_name", "phone_number", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Ismingizni kiriting", "class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Telefon raqamingiz", "class": "form-control"}),
            "message": forms.Textarea(attrs={"placeholder": "Xabaringizni kiriting", "class": "form-control", "rows": 4}),
        }

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", [])
        super().__init__(*args, **kwargs)

        for question in questions:
            choices = [
                (1, question.option1),
                (2, question.option2),
                (3, question.option3),
                (4, question.option4),
            ]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, label=question.question_text, required=True
            )