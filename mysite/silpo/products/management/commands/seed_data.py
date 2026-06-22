import os
import requests
import uuid
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from categories.models import Category
from products.models import Product, ProductImage
from users.utils import save_custom_image


class Command(BaseCommand):
    help = 'Seed database with test data for products and categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_existing_data()
        
        self.stdout.write(self.style.SUCCESS('🚀 Starting seed data...'))
        self.create_seed_data()
        self.stdout.write(self.style.SUCCESS('✅ Seed data successfully created!'))

    def clear_existing_data(self):
        """Delete all categories and products"""
        self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.clear_image_folder(settings.IMAGES_ROOT / 'products')
        self.clear_image_folder(settings.IMAGES_ROOT / 'categories')
        self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

    def clear_image_folder(self, folder_path):
        """Remove all files from an image folder and keep the folder itself."""
        os.makedirs(folder_path, exist_ok=True)
        for entry in os.scandir(folder_path):
            if entry.is_file() or entry.is_symlink():
                os.remove(entry.path)
            elif entry.is_dir():
                self.clear_image_folder(entry.path)
                os.rmdir(entry.path)

    def create_seed_data(self):
        """Create all categories and products with images"""
        
        seed_data = {
            'Овочі': {
                'description': 'Свіжі органічні овочі',
                'slug': 'vegetables',
                'image_url': 'https://images.silpo.ua/v2/categories/200x200/webp/_pos--right_/986f891f-ffd9-4224-8927-41a0eb5ccbc1.png',
                'products': {
                    'Помідори': {
                        'slug': 'pomidory',
                        'description': 'Сочні червоні помідори, вирощені в теплиці',
                        'price': 45.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/68622333-6dd6-40c4-8f30-5b97340dc168.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/e39f8776-dc36-4274-94b1-7031cf097b32.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/ee915f60-f397-4949-9bd2-15d01edbd88f.png',
                        ]
                    },
                    'Огірки': {
                        'slug': 'ohirky',
                        'description': 'Хрусткі зелені огірки',
                        'price': 35.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/4e8b47fc-6740-4e7d-80bd-13d7e0f6ddd1.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/6b1f8aad-a184-4638-9379-ece9903329c4.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/d8776b28-ffe7-4cb3-ad7d-de37532eea57.png',
                        ]
                    },
                    'Болгарський перець': {
                        'slug': 'bolharskyi-perets',
                        'description': 'Солодкий болгарський перець різних кольорів',
                        'price': 50.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/f5b684a9-ac31-4707-bf18-9c641c78368d.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/cea08f1c-ae7e-4a1a-ad7e-2e7bcdbb3e06.jpg',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/6a3ca7c8-04c9-444a-82ac-2c4c8d68a395.jpg',
                        ]
                    },
                }
            },
            'Фрукти': {
                'description': 'Сочні спілі фрукти прямо з саду',
                'slug': 'fruits',
                'image_url': 'https://images.silpo.ua/v2/categories/200x200/webp/_pos--right_/aa8c41de-6ffd-4b7c-9e86-999a2d249dfa.png',
                'products': {
                    'Яблука': {
                        'slug': 'yabluka',
                        'description': 'Червоні хрусткі яблука, багаті на вітаміни',
                        'price': 40.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/109ba4e7-8515-409c-91d9-a452fafdfb92.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/aa6a8c93-33f6-4ba5-b8e2-b400918e4b9e.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/a2415de2-7ff1-4e89-be9b-168ef7819e13.png',
                        ]
                    },
                    'Банани': {
                        'slug': 'banany',
                        'description': 'Спілі м\'які банани',
                        'price': 30.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/f5214071-6d83-4de8-b655-b977809cf880.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/fe11c917-6f9d-42f3-b2be-aadd83cf118f.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/208fac41-53f8-4823-a6f0-d0627cfc663b.png',
                        ]
                    },
                    'Апельсини': {
                        'slug': 'apelsyny',
                        'description': 'Солодкі сочні апельсини, багаті на C вітамін',
                        'price': 55.00,
                        'images': [
                            'https://images.silpo.ua/v2/products/1000x1000/webp/7774efde-6f1a-4ea6-821f-1ecb3b4d34fb.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/6ad7b56f-dc6d-4577-9005-ce3220d4bf15.png',
                            'https://images.silpo.ua/v2/products/1000x1000/webp/0260ba1e-6416-44b9-b5a3-11395d8bd44a.png',
                        ]
                    },
                }
            }
        }
        
        for category_name, category_data in seed_data.items():
            self.create_category_with_products(category_name, category_data)

    def create_category_with_products(self, category_name, category_data):
        """Create a category with its products and images"""
        
        category, created = Category.objects.update_or_create(
            slug=category_data['slug'],
            defaults={
                'name': category_name,
                'description': category_data['description'],
            },
        )

        self.create_category_image(category, category_data['image_url'])
        
        status = '✨ created' if created else '✓ already exists'
        self.stdout.write(self.style.SUCCESS(f"📁 Category '{category_name}' {status}"))
        
        for product_name, product_data in category_data['products'].items():
            self.create_product_with_images(category, product_name, product_data)

    def create_product_with_images(self, category, product_name, product_data):
        """Create a product with images"""
        
        # Generate unique slug
        slug_attempt = product_data.get('slug') or slugify(product_name, allow_unicode=False)
        if not slug_attempt:
            slug_attempt = 'product'
        product_slug = f"{slug_attempt}-{str(uuid.uuid4())[:8]}"
        
        product, created = Product.objects.get_or_create(
            name=product_name,
            category=category,
            defaults={
                'slug': product_slug,
                'description': product_data['description'],
                'price': product_data['price']
            }
        )
        
        status = '✨ created' if created else '✓ already exists'
        self.stdout.write(f"  🛒 Product '{product_name}' {status}")
        
        # Download and create images
        for priority, image_url in enumerate(product_data['images']):
            self.create_product_image(product, priority, image_url)

    def create_product_image(self, product, priority, image_url):
        """Download and create a product image"""
        
        # Check if image already exists
        if ProductImage.objects.filter(product=product, priority=priority).exists():
            self.stdout.write(f"    ⏭️  Image [priority {priority}] already exists")
            return
        
        try:
            # Download image from URL
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Get file extension
            content_type = response.headers.get('content-type', '')
            ext = self.get_extension_from_content_type(content_type, image_url)
            
            # Create file name
            filename = f"products/{product.slug}_img_{priority}{ext}"
            
            # Create ProductImage
            image = ProductImage(
                product=product,
                priority=priority
            )
            image.image.save(
                filename,
                ContentFile(response.content),
                save=True
            )
            
            self.stdout.write(self.style.SUCCESS(
                f"    ✅ Image [priority {priority}] downloaded"
            ))
            
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(
                f"    ❌ Failed to download image [priority {priority}]: {str(e)}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"    ❌ Error creating image [priority {priority}]: {str(e)}"
            ))

    def create_category_image(self, category, image_url):
        """Download and save category image to images/categories like manual category create."""
        existing_name = category.image
        existing_path = None
        if existing_name and not existing_name.startswith('http'):
            existing_path = settings.IMAGES_ROOT / 'categories' / existing_name
            if existing_path.exists():
                self.stdout.write("  ⏭️  Category image already exists")
                return

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            content_type = response.headers.get('content-type', '')
            ext = self.get_extension_from_content_type(content_type, image_url)

            temp_file = ContentFile(response.content, name=f"{category.slug}{ext}")
            image_name = save_custom_image(temp_file, size=(600, 600), folder='categories')

            # Keep deterministic latin filename for seeded category images.
            final_name = f"{category.slug}.webp"
            random_path = settings.IMAGES_ROOT / 'categories' / image_name
            final_path = settings.IMAGES_ROOT / 'categories' / final_name
            if final_path.exists():
                final_path.unlink()
            os.replace(random_path, final_path)

            category.image = final_name
            category.save(update_fields=['image'])

            if existing_path and existing_path.exists() and existing_path.name != image_name:
                existing_path.unlink()

            self.stdout.write(self.style.SUCCESS("  ✅ Category image downloaded"))
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(
                f"  ❌ Failed to download category image: {str(e)}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"  ❌ Error creating category image: {str(e)}"
            ))

    def get_extension_from_content_type(self, content_type, url):
        """Get file extension from content type or URL"""
        ext_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/webp': '.webp',
            'image/gif': '.gif'
        }
        
        ext = ext_map.get(content_type, '.webp')
        
        # Try to get from URL
        if '.' in url.split('/')[-1]:
            url_ext = '.' + url.split('.')[-1].split('?')[0]
            if url_ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                ext = url_ext
        
        return ext