from django.db import models

from categories.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField(upload_to="images/")
    priority = models.PositiveIntegerField(default=0, help_text="0 - Головне фото")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'created_at']
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Фото [{self.priority}] для {self.product.name}"
 
 