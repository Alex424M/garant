import re
from django import forms
from .models import Application
from django.contrib.auth.models import User
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['phone', 'message']
        
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not re.match(r'^\+?\d{10,15}$', phone):
            raise forms.ValidationError(
                "Введите корректный номер телефона (10–15 цифр)."
            )

        return phone

    def clean_message(self):
        message = self.cleaned_data.get("message")

        if len(message) > 500:
            raise forms.ValidationError(
                "Комментарий не должен превышать 500 символов."
            )

        return message
class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()

        if not re.fullmatch(r"[А-Яа-яЁё\-]+", first_name):
            raise forms.ValidationError("Имя должно содержать только русские буквы.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()

        if not re.fullmatch(r"[А-Яа-яЁё\-]+", last_name):
            raise forms.ValidationError("Фамилия должна содержать только русские буквы.")

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("Пароль минимум 8 символов.")

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Пароль должен содержать заглавную букву.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Пароли не совпадают.")