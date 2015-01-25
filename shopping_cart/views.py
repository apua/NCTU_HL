# -*- coding=utf8 -*-

import os
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory

from .models import Product, Record, Contact
from information.models import Information


class AmountForm(forms.Form):
    pid = forms.IntegerField()
    pid.widget.attrs.update({'hidden':'hidden'}) # hidden and POST back
    #amount = forms.fields_for_model(Record)['amount']
    #amount.widget.attrs.update({'required':'required'}) # check by Chrome browser
    amount = forms.ChoiceField(choices = [(i,i) for i in range(10)])


def amountformset_factory(user, amountdata, form=AmountForm):
    FormSet = formset_factory(AmountForm, extra=0)

    class AmountFormSet(FormSet):
        def __init__(self, *args, **kwargs):
            kwargs['initial'] = [
                # since amount field is a choice field, the type of post value of amount would be string
                {'pid': pid, 'amount': amountdata[pid]['amount']}
                for pid in sorted(amountdata)
            ]
            super(AmountFormSet, self).__init__(*args, **kwargs)
            self.supinfo = {
                'product': Product._meta.get_field('name').verbose_name,
                'price':   Product._meta.get_field('price').verbose_name,
                'amount':  Record._meta.get_field('amount').verbose_name,
                }
            for form in self:
                D = amountdata[int(form['pid'].value())]
                form.supinfo= {'name': D['name'], 'price': D['price']}

        def clean(self):
            pass

        def save(self, commit=True):
            self.deleted = []
            changedData = {
                int(form.cleaned_data['pid']):int(form.cleaned_data['amount'])
                for form in self if form.has_changed()
            }
            if not changedData:
                return []
            existingIns = Record.objects.filter(user=user)
            if not existingIns:
                obj_constuct = Record.objects.create if commit else Record
                return [obj_constuct(user=user,product_id=pid,amount=amount)
                        for pid,amount in changedData.items()]

            existingPid = set(sum(existingIns.values_list('product_id'),()))
            toZeroPid = {pid for pid in changedData if changedData[pid]==0}
            updatedPid = changedData.viewkeys() - toZeroPid
            newPid = changedData.viewkeys() - existingPid

            deletedIns = existingIns.filter(product_id__in=toZeroPid)
            updatedIns = existingIns.filter(product_id__in=updatedPid)

            self.deleted_objects = [obj for obj in deletedIns]
            newIns = [Record(user=user,product_id=pid,amount=changedData[pid])
                      for pid in newPid]
            updatedIns = [ins.__setattr__('amount',changedData[ins.product_id])
                          or ins for ins in updatedIns]
            instances = newIns + updatedIns
            
            if commit:
                deletedIns.delete()
                for ins in instances:
                    ins.save()

            return instances

    return AmountFormSet


@login_required(login_url='/login/')
def order(request):

    # define template location
    template =         os.path.join(__package__,'order_form.html')
    contact_template = os.path.join(__package__,'contact_form.html')
    amount_template =  os.path.join(__package__,'amount_form.html')

    # readonly or not
    info = Information.objects.first()
    order_start, order_end = info.order_st, info.order_ed
    today = datetime.now().date()
    user = request.user
    readonly = not (user.is_superuser or order_start <= today <= order_end )

    # generate form/formset class
    ContactForm = modelform_factory(Contact, exclude=['user'])
    AmountFormSet = amountformset_factory(user=user, amountdata=Record.objects.get_formset_data(user=user))

    if request.method=='POST' and not readonly:
        contact_form = ContactForm(request.POST, prefix='contact')
        amount_formset = AmountFormSet(request.POST, prefix='order')
        if contact_form.is_valid() and amount_formset.is_valid():
            # save contact form
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            # save amount form set
            amount_formset.save()
    else:
        contact_form = ContactForm(instance=Contact.objects.filter(user=user).first(), prefix='contact')
        amount_formset = AmountFormSet(prefix='order')

    # handler when view is readonly
    if readonly:
        for field in contact_form.fields.viewvalues():
            field.widget = forms.TextInput(attrs={'disabled':'disabled'})
        for form in amount_formset:
            form['amount'].field.widget = forms.TextInput(attrs={'disabled':'disabled'})

    # render template
    context = {
        'readonly': readonly,
        'contact_form': contact_form,
        'amount_formset': amount_formset,
        'contact_template': contact_template,
        'amount_template': amount_template,
        } 
    return render(request, template, context)
