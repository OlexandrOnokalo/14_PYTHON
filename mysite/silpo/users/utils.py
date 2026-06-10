import os # для роботи з папками і файлами
from django.conf import settings #Налаштування конфігурації Django
from PIL import Image # для роботи з зображеннями
import io # для роботи з байтами
import uuid # для генерації унікальних імен файлів
from django.core.files.base import ContentFile # файл який передав користувач

def compress_image(image_field, size=(800,800),quality=85):
    # якщо фото у PNG, конвертуємо його в RGB для JPEG
    image = Image.open(image_field).convert('RGB') 
    # зберігає оригінальне співвідношення сторін
    image.thumbnail(size, Image.LANCZOS)
    # створюємо унікальне ім'я файлу
    uid = str(uuid.uuid4())[:10] # 10 символів назви
    image.name='{}.weebp'.format(uid) # змінюємо розширення на webp
    # зберігаємо стиснуте зображення в пам'яті
    output = io.BytesIO()
    # перетворюємо зображення в формат WEBP з заданою якістю
    image.save(output, format='WEBP', quality=quality)
    # зміщаємось на початок потока, щоб читати з самого початку
    output.seek(0)

    # отримуємо саме фото
    resized_image = ContentFile(output.getvalue())
    # повертаємо стиснуте зображення і назву
    return resized_image, image.name

def save_custom_image(image, size, folder):
    resized_image, image_name = compress_image(image, size)
    # Створюємо шлях до директорії та шлях до файлу
    dir_path = os.path.join(settings.IMAGES_ROOT, folder)
    full_path = os.path.join(dir_path, image_name)
    # Створюємо папки, якщо їх ще не існує
    os.makedirs(dir_path, exist_ok=True)
    # Зберігаємо файл
    with open(full_path, "wb") as f:
        f.write(resized_image.read())
    return image_name