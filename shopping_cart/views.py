# -*- coding=utf8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shopping_cart.models import Product, Record, Contact, ContactForm

@login_required(login_url='/login/')
def order(request):
    if request.method=='POST':
        Record.objects.save_amount_list(request.user, request.POST)
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = request.user
            ins.save()
        context = {
            'order': Record.objects.get_amount_list(user=request.user),
            'contact_form': contact_form,
        }
        return render(request, 'shopping_cart/order_form.html', context)
    else:
        user = request.user
        contact = Contact.objects.get_or_None(user=user)
        order = Record.objects.get_amount_list(user=user)
        context = {
            'order': order,#.order_by('id'),
            'contact_form': ContactForm(instance=contact),
        }
        return render(request, 'shopping_cart/order_form.html', context)
