from django.shortcuts import render

from products.models import Product


# Create your views here.
def show_products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, "products.html", {"products": products})
 