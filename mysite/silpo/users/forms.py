from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm


class CustomUserRegisterForm(UserCreationForm):

    email = forms.EmailField(
        label='Електронна пошта',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'example@gmail.com'
        })
    )

    first_name = forms.CharField(
        label='Ім\'я',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Вкажіть ім\'я'
        })
    )

    last_name = forms.CharField(
        label='Прізвище',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Вкажіть прізвище'
        })
    )

    image = forms.ImageField(
        label='Зображення',
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-400 '
                     'file:mr-4 file:py-2 file:px-4 '
                     'file:rounded-lg file:border-0 '
                     'file:text-sm file:font-semibold '
                     'file:bg-indigo-600 file:text-white '
                     'hover:file:bg-indigo-500 '
                     'cursor-pointer',
            'accept': 'image/*',
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Вкажіть пароль'
        })
    )

    password2 = forms.CharField(
        label='Повторіть пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Повтор пароля'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name','image', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Дана пошта уже зареєстрована")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")
        return password2

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Електронна пошта',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'example@gmail.com'
        })
    )

    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Вкажіть пароль'
        })
    )

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'example@gmail.com'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувача з такою поштою не знайдено")
        return email

    def save(self, request):
        email = self.cleaned_data['email']
        user = CustomUser.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(
            f'/users/reset/{uid}/{token}/'
        )

        subject = 'Відновлення пароля'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        send_mail(subject, message, None, [email])


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Вкажіть новий пароль'
        })
    )

    new_password2 = forms.CharField(
        label='Повторіть пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none',
            'placeholder': 'Повторіть новий пароль'
        })
    )