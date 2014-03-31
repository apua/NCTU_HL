# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms.models import modelform_factory, modelformset_factory, formset_factory
from django.forms import Form, fields_for_model, ValidationError

from shopping_cart.models import Product, Record, Contact


class AmountForm(Form):
    _product_fields = fields_for_model(Product)
    _record_field = fields_for_model(Record)

    product = _product_fields['name']
    price = _product_fields['price']
    amount = _record_field['amount']

    product.widget.attrs.update({'disabled':'disabled'})
    price.widget.attrs.update({'disabled':'disabled'})

    product.required = price.required = False


@login_required(login_url='/login/')
def order(request):
    user = request.user
    app_dir = 'shopping_cart'
    template = os.path.join(app_dir, 'order_form.html')
    ContactForm = modelform_factory(Contact, exclude=['user'])
    #test_formset = modelformset_factory(model=Product)()
    test_formset = formset_factory(form=AmountForm, extra=10)

    if request.method=='POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            Record.objects.save_amount_list(user, request.POST)
        order = Record.objects.get_amount_list(user=user)
        test_form = AmountForm(request.POST)
    else:
        contacts = Contact.objects.filter(user=user)
        contact_form = ContactForm(
            instance = contacts[0] if contacts else None,
            prefix = 'contact',
            )
        order = Record.objects.get_amount_list(user=user)
        test_form = AmountForm()

    context = {
        'order': order,
        'contact_form': contact_form,
        'contact_template': os.path.join(app_dir,'contact_form.html'),
        'amount_template': os.path.join(app_dir,'amount_form.html'),
        'test': test_form,
        'test_formset': test_formset,
        } 
    return render(request, template, context)
