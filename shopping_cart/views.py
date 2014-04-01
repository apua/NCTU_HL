# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import Form, fields_for_model, ValidationError
from django.forms.models import modelform_factory

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

from django.forms.formsets import BaseFormSet, formset_factory

class AmountFormSet(BaseFormSet):
    pass


def amountformset_factory(form, user, productmodel=Product, recordmodel=Record):
    u"""一些變數可能得再參照原始碼"""

    products = productmodel.objects.all() #may filte which visible
    records = recordmodel.objects.filter(product__in=products, user=user)
    amounts = {r.product: r.amount for r in records}
    data = [{'product': p.name, 'price':p.price, 'amount':amounts.get(p,0)} for p in products]
    FormSet = formset_factory(AmountForm, extra=0)

    class AmountFormSet(FormSet):
        def __init__(self, *args, **kwargs):
            kwargs['initial'] = data
            super(AmountFormSet, self).__init__(*args, **kwargs)

    return AmountFormSet

#amountformset_factory = formset_factory


@login_required(login_url='/login/')
def order(request):
    user = request.user
    app_dir = 'shopping_cart'
    template = os.path.join(app_dir, 'order_form.html')
    ContactForm = modelform_factory(Contact, exclude=['user'])

    #AmountFormSet = amountformset_factory(form=AmountForm)
    AmountFormSet = amountformset_factory(form=AmountForm, user=user)

    if request.method=='POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            Record.objects.save_amount_list(user, request.POST)
        order = Record.objects.get_amount_list(user=user)
        test_form = AmountForm(request.POST, prefix='a')
        test_formset = AmountFormSet(request.POST, prefix='b')
    else:
        contacts = Contact.objects.filter(user=user)
        contact_form = ContactForm(
            instance = contacts[0] if contacts else None,
            prefix = 'contact',
            )
        order = Record.objects.get_amount_list(user=user)
        test_form = AmountForm(prefix='a')
        test_formset = AmountFormSet(prefix='b')

    context = {
        'order': order,
        'contact_form': contact_form,
        'contact_template': os.path.join(app_dir,'contact_form.html'),
        'amount_template': os.path.join(app_dir,'amount_form.html'),
        'test_form': test_form,
        'test_formset': test_formset,
        } 
    return render(request, template, context)
