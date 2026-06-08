import io
import os
from PIL import Image
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

from users.forms import CustomUserForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():

            # prepare instance but don't save yet
            user = form.save(commit=False)

            # ensure we have a username (DB has unique constraint)
            email = form.cleaned_data.get('email') or getattr(user, 'email', '') or ''
            username = getattr(user, 'username', '') or ''
            if not username:
                base = (email.split('@')[0] if email else f"{getattr(user,'first_name','')}.{getattr(user,'last_name','')}".strip())
                base = base or 'user'
                base = base.replace(' ', '_').lower()
                UserModel = get_user_model()
                new_username = base
                i = 0
                while UserModel.objects.filter(username=new_username).exists():
                    i += 1
                    new_username = f"{base}{i}"
                user.username = new_username

            # if form provided raw password fields, set hashed password
            pwd = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
            if pwd:
                try:
                    user.set_password(pwd)
                except Exception:
                    pass

            uploaded = form.cleaned_data.get('image') or request.FILES.get('image')
            if uploaded:
                # ensure file pointer at start
                try:
                    uploaded.seek(0)
                except Exception:
                    try:
                        uploaded.file.seek(0)
                    except Exception:
                        pass

                try:
                    img = Image.open(uploaded)
                    img.verify()
                    # reopen because verify() can leave the file closed
                    try:
                        uploaded.seek(0)
                    except Exception:
                        try:
                            uploaded.file.seek(0)
                        except Exception:
                            pass
                    img = Image.open(uploaded)
                except Exception:
                    messages.error(request, 'Неможливо прочитати завантажене зображення.')
                    return render(request, 'register.html', {'form': form})

                # convert to RGB for JPEG
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                sizes = {
                    'image_small': (100, 100),
                    'image_medium': (300, 300),
                    'image_big': (800, 800),
                }

                base_name, _ext = os.path.splitext(uploaded.name)
                for field_name, size in sizes.items():
                    im_copy = img.copy()
                    try:
                        resample_filter = Image.Resampling.LANCZOS
                    except AttributeError:
                        # Pillow < 10: LANCZOS or ANTIALIAS
                        resample_filter = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', 1))

                    im_copy.thumbnail(size, resample=resample_filter)

                    buf = io.BytesIO()
                    im_copy.save(buf, format='JPEG', quality=85)
                    buf.seek(0)

                    file_name = f"{base_name}_{field_name}.jpg"
                    content_file = ContentFile(buf.getvalue(), name=file_name)

                    field_obj = getattr(user, field_name, None)
                    if field_obj is not None and hasattr(field_obj, 'save'):
                        # model has ImageField/FileField
                        try:
                            field_obj.save(file_name, content_file, save=False)
                        except Exception:
                            # fallback: save to default storage and set path
                            saved_path = default_storage.save(os.path.join('users', file_name), content_file)
                            setattr(user, field_name, saved_path)
                    else:
                        # field is not a FileField (e.g. CharField) — save file and store path string
                        saved_path = default_storage.save(os.path.join('users', file_name), content_file)
                        setattr(user, field_name, saved_path)

            # save instance and any m2m from form
            user.save()
            try:
                form.save_m2m()
            except Exception:
                pass

            messages.success(request, 'Реєстрація пройшла успішно!')
            return redirect('homepage')
        else:
            messages.error(request, 'Помилка реєстрації. Будь ласка, перевірте введені дані.')
    else:
        form = CustomUserForm()
    return render(request, 'register.html', {'form': form})