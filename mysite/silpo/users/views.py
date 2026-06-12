from django.shortcuts import render, redirect
from django.contrib import messages

from users.forms import CustomUserRegisterForm, CustomUserLoginForm
from .utils import save_custom_image
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #Обробимо форму, що заповнив користувач
                user = form.save(commit=False)
                #Якщо користувач змінив email, оновимо username, щоб він збігався з email
                if 'email' in form.changed_data:
                    user.username = form.cleaned_data['email']
                #Якщо користувач завантажив зображення, обробимо його і збережемо у різних розмірах
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    user.image_small = save_custom_image(image,size=(300,300), folder='small')
                    user.image_medium = save_custom_image(image,size=(800,800), folder='medium')
                    user.image_large = save_custom_image(image,size=(1200,1200), folder='large')
                user.save()
                login(request, user)
                return redirect('homepage')
            except Exception as e:
                messages.error(request, f'Щось пішло не так: {str(e)}')
        else:
            messages.info(request, 'Виникли помилки при заповненні форми')
    else:
        form = CustomUserRegisterForm()

    return render(request, "register.html", {"form": form})
 
# def user_login(request):
#     if request.method == 'POST':
#         form = CustomUserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['username'],
#                                 password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect('homepage')
#             else:
#                 print("---user not found---")
#         else:
#             form.add_error(None, "Невірний email або пароль")
#             print("---form not valid---")
#     else:
#         form = CustomUserLoginForm()
#     return render(request, 'login.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
        else:
            form.add_error(None, "Логін або пароль вказано невірно")
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('homepage')