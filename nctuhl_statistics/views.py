from django.shortcuts import render

from shopping_cart.models import Product, Record

import os

# Create your views here.
def statistics_index (request):
    template = os.path.join(__package__,'stat_index.html')
    context = { }
    return render(request, template, context)

def statistics_products (request):
    template = os.path.join(__package__,'stat_products.html')

    result = {i.name: 0 for i in Product.objects.all()}

    for i in Record.objects.all():
        result[i.product.name] += i.amount

    context = {
        'results': result
    }
    return render(request, template, context)
