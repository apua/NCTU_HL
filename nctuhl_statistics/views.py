from django.shortcuts import render

from shopping_cart.models import Product, Record, Contact
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import os

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

# Create your views here.
@login_required(login_url='/login/')
def stat_index (request):
    if not request.user.is_siteadmin:
        return HttpResponseRedirect(reverse('index'))
    template = os.path.join(__package__,'stat_index.html')
    context = { }
    return render(request, template, context)

@login_required(login_url='/login/')
def stat_products (request):
    if not request.user.is_siteadmin:
        return HttpResponseRedirect(reverse('index'))
    template = os.path.join(__package__,'stat_products.html')

    result = {i.name: 0 for i in Product.objects.all()}

    for i in Record.objects.all():
        result[i.product.name] += i.amount

    context = {
        'results': result
    }
    return render(request, template, context)

@login_required(login_url='/login/')
def stat_dorms (request):
    if not request.user.is_siteadmin:
        return HttpResponseRedirect(reverse('index'))
    template = os.path.join(__package__,'stat_dorms.html')

    dorm_ids = [i.dorm for i in Contact.objects.all()]

    context = {
        'results': sorted([ (dorm_table[i], dorm_ids.count(i)) for i in dorm_table ], key=lambda x:x[0])
    }
    return render(request, template, context)

@login_required(login_url='/login/')
def stat_print (request):
    if not request.user.is_siteadmin:
        return HttpResponseRedirect(reverse('index'))
    template = os.path.join(__package__,'stat_print.html')
    table = [{
            'name':  i.name,
            'email': i.user.email,
            'dorm':  dorm_table[i.dorm],
            'room':  i.room,
            'phone': i.phone,
        } for i in Contact.objects.all()]
    context = {
        'table': table
    }
    return render(request, template, context)
