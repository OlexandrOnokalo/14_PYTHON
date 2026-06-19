import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from categories.forms import CategoryForm
from categories.models import Category
from django.contrib import messages

from users.utils import save_custom_image

# Create your views here.

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories/category_list.html',{ 'categories': categories })

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                if not category.slug:
                    category.slug = slugify(category.name, allow_unicode=False)
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    image_name = save_custom_image(image, size=(600,600), folder='categories')
                    category.image=image_name
                category.save()
                messages.success(request, 'Category created successfully')
                return redirect('categories:list')

            except Exception as e:
                messages.error(request, f'Помилка створення категорії {str(e)}')
        else:
            messages.error(request,'Виправте помилки у формі')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_create.html',{ 'form': form })


def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        try:
            if category.image:
                file_path = settings.BASE_DIR / 'images' / 'categories' / category.image
                if file_path.exists():
                    file_path.unlink()

            category.delete()
            messages.success(request, 'Категорію та її зображення успішно видалено')

        except Exception as x:
            messages.error(request, f'Помилка при видаленні категорії: {str(x)}')

    return redirect('categories:list')

def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    old_image_name = category.image

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                category = form.save(commit=False)

                if 'image' in request.FILES:
                    image = request.FILES['image']

                    new_image_name = save_custom_image(image, size=(600, 600), folder='categories')
                    category.image = new_image_name

                    if old_image_name:
                        old_file_path = os.path.join(settings.BASE_DIR, 'images', 'categories', old_image_name)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                else:
                    category.image = old_image_name

                category.save()
                messages.success(request, 'Категорію успішно оновлено')
                return redirect('categories:list')

            except Exception as x:
                messages.error(request, f'Помилка редагування категорії: {str(x)}')
        else:
            messages.error(request, 'Виправте помилки у формі')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/category_edit.html', {'form': form, 'category': category})
 