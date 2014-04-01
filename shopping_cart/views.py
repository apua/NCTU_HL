# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory

from models import Product, Record, Contact


class AmountForm(forms.Form):
    pid = forms.IntegerField()
    pid.widget.attrs.update({'hidden':'hidden'}) # hidden and POST back
    #amount = forms.fields_for_model(Record)['amount']
    #amount.widget.attrs.update({'required':'required'}) # check by Chrome browser
    amount = forms.ChoiceField(choices = [(i,i) for i in range(10)])


def amountformset_factory(user, amountdata, form=AmountForm):
    """
    """
    FormSet = formset_factory(AmountForm, extra=0)

    class AmountFormSet(FormSet):
        """
        """
        def __init__(self, *args, **kwargs):
            kwargs['initial'] = [{'pid': pid, 'amount': amountdata[pid]['amount']} for pid in sorted(amountdata)]
            super(AmountFormSet, self).__init__(*args, **kwargs)

        def clean(self):
            pass

        def save(self, commit=True):
            """
            """
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


@login_required(login_url='/login/')
def order(request):

    # define template location
    template =         os.path.join(__package__,'order_form.html')
    contact_template = os.path.join(__package__,'contact_form.html')
    amount_template =  os.path.join(__package__,'amount_form.html')

    user = request.user
    # get amount data
    _records = { r.product: r.amount for r in Record.objects.filter(user=user) }
    _amounts = { p.id: {'amount': _records.get(p,0), 'name': p.name, 'price': p.price}
                 for p in Product.objects.all() }
 
    # generate form/formset class
    ContactForm = modelform_factory(Contact, exclude=['user'])
    AmountFormSet = amountformset_factory(user=user, amountdata=_amounts)

    if request.method=='POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        amount_formset = AmountFormSet(request.POST, prefix='b')
        if contact_form.is_valid() and amount_formset.is_valid():
            # save contact form
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            # save amount form set
            amount_formset.save()
    else:
        contacts = Contact.objects.filter(user=user)
        contact_form = ContactForm(instance=contacts[0] if contacts else None, prefix='contact')
        amount_formset = AmountFormSet(prefix='b')

    # generate formset supplementary information
    for form in amount_formset:
        D = _amounts[int(form['pid'].value())]
        form.supinfo= {'name': D['name'], 'price': D['price']}
    amount_formset.supinfo = { 'product': u'PRODUCT',
                               'price':   u'PRICE',
                               'amount':  u'AMOUNT',  }

    context = {
        'contact_form': contact_form,
        'amount_formset': amount_formset,
        'contact_template': os.path.join(__package__,'contact_form.html'),
        'amount_template': os.path.join(__package__,'amount_form.html'),
        } 
    return render(request, template, context)
