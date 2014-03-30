# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shopping_cart.models import Product, Record, Contact
from django.forms.models import modelformset_factory


@login_required(login_url='/login/')
def order(request):
    user = request.user
    app_dir = 'shopping_cart'
    template = os.path.join(app_dir, 'order_form.html')
    ContactFormSet = modelformset_factory(Contact, exclude=['user'])

    if request.method=='POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            Record.objects.save_amount_list(user, request.POST)
        order = Record.objects.get_amount_list(user=user)
    else:
        contact_form = ContactFormSet(
            queryset=Contact.objects.filter(user=user),
            prefix='contact'
            )[0]
        order = Record.objects.get_amount_list(user=user)

    context = {
        'order': order,
        'contact_form': contact_form,
        'contact_template': os.path.join(app_dir,'contact_form.html'),
        'amount_template': os.path.join(app_dir,'amount_form.html'),
        }
    return render(request, template, context)
