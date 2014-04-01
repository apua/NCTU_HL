# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms
from django.forms import Form, fields_for_model, ValidationError
from django.forms.models import modelform_factory
from django.forms.formsets import BaseFormSet, formset_factory

from shopping_cart.models import Product, Record, Contact


class AmountForm(Form):
    pid = forms.IntegerField()
    pid.widget.attrs.update({'hidden':'hidden'}) # hidden and POST back
    amount = fields_for_model(Record)['amount']
    amount.widget.attrs.update({'required':'required'}) # check by Chrome browser
    #amount = forms.ChoiceField(choices = [(i,i) for i in range(10)])


def amountformset_factory(user, amountdata, form=AmountForm):
    FormSet = formset_factory(AmountForm, extra=0)

    class AmountFormSet(FormSet):

        def __init__(self, *args, **kwargs):
            kwargs['initial'] = [{'pid': pid, 'amount': amountdata[pid]['amount']} for pid in sorted(amountdata)]
            super(AmountFormSet, self).__init__(*args, **kwargs)

        def clean(self):
            pass

        def save(self, commit=True):
            changed_data = {
                int(form.cleaned_data['pid']):int(form.cleaned_data['amount'])
                for form in self.initial_forms
                if form.has_changed()
            }

            if not changed_data:
                return []

            empty_pid = {pid for pid in changed_data if changed_data[pid]==0 }
            deleted_objects = Record.objects.filter(user=user,product_id__in=empty_pid )
            self.deleted_objects = [obj for obj in deleted_objects]
            
            nonempty_pid = changed_data.viewkeys() - empty_pid
            saved_obj = Record.objects.filter(user=user, product_id__in=nonempty_pid)
            for obj in saved_obj: obj.amount = changed_data[obj.product_id]
            instances = [obj for obj in saved_obj] + [Record(user=user,product_id=pid,amount=changed_data[pid])
                for pid in nonempty_pid - {obj.product_id for obj in saved_obj}]

            if commit:
                deleted_objects.delete()
                for obj in instances: obj.save()

            return instances
            

    return AmountFormSet



def get_amount(user):
    records = {r.product: r.amount for r in Record.objects.filter(user=user)}
    return { p.id: {'amount': records.get(p,0), 'name': p.name, 'price': p.price}
             for p in Product.objects.all() }


@login_required(login_url='/login/')
def order(request):
    user = request.user
    app_dir = 'shopping_cart'
    template = os.path.join(app_dir, 'order_form.html')
    ContactForm = modelform_factory(Contact, exclude=['user'])

    # get amount data
    _records = { r.product: r.amount for r in Record.objects.filter(user=user) }
    _amounts = { p.id: {'amount': _records.get(p,0), 'name': p.name, 'price': p.price}
                 for p in Product.objects.all() }
 
    AmountFormSet = amountformset_factory(user=user, amountdata=_amounts)

    if request.method=='POST':
        #print request.POST
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            Record.objects.save_amount_list(user, request.POST)
        order = Record.objects.get_amount_list(user=user)
        test_form = AmountForm(request.POST, prefix='a')
        test_formset = AmountFormSet(request.POST, prefix='b')

        #for idx, form in enumerate(test_formset):
        #    print idx, form.has_changed(), form.changed_data

        if test_formset.is_valid():
            test_formset.save()

    else:
        contacts = Contact.objects.filter(user=user)
        contact_form = ContactForm(
            instance = contacts[0] if contacts else None,
            prefix = 'contact',
            )
        order = Record.objects.get_amount_list(user=user)
        test_formset = AmountFormSet(prefix='b')


    # generate formset extra information
    for form in test_formset:
        D = _amounts[int(form['pid'].value())]
        form.informations = {'name': D['name'], 'price': D['price']}
    test_formset.informations = { 'product': u'PRODUCT',
                                  'price':   u'PRICE',
                                  'amount':  u'AMOUNT',
                                }

    context = {
        'order': order,
        'contact_form': contact_form,
        'contact_template': os.path.join(app_dir,'contact_form.html'),
        'amount_template': os.path.join(app_dir,'amount_form.html'),
        'test_formset': test_formset,
        } 
    return render(request, template, context)
