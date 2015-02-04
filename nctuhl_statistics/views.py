from django.shortcuts import render

from shopping_cart.models import Product, Record, Contact

import os

# Create your views here.
def stat_index (request):
    template = os.path.join(__package__,'stat_index.html')
    context = { }
    return render(request, template, context)

def stat_products (request):
    template = os.path.join(__package__,'stat_products.html')

    result = {i.name: 0 for i in Product.objects.all()}

    for i in Record.objects.all():
        result[i.product.name] += i.amount

    context = {
        'results': result
    }
    return render(request, template, context)

def stat_dorms (request):
    template = os.path.join(__package__,'stat_dorms.html')

    dorm_ids = [i.dorm for i in Contact.objects.all()]
    dorm_table = {
         0: u'外宿',
        85: u'竹軒',
        88: u'女二',
        77: u'七舍',
        78: u'八舍',
        79: u'九舍',
        80: u'十舍',
        81: u'11舍',
        82: u'12舍',
        83: u'13舍',
        84: u'研一',
        87: u'研二',
    }

    context = {
        'results': sorted([ (dorm_table[i], dorm_ids.count(i)) for i in dorm_table ], key=lambda x:x[0])
    }
    return render(request, template, context)
