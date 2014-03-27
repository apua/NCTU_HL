# -*- coding=utf8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shopping_cart.models import Product, Record, Contact, ContactForm

@login_required(login_url='/login/')
def order(request):
    user = request.user
    template = 'shopping_cart/order_form.html'
    if request.method=='POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            ins = contact_form.save(commit=False)
            ins.user = user
            ins.save()
            Record.objects.save_amount_list(user, request.POST)
        order = Record.objects.get_amount_list(user=user)
    else:
        contact = Contact.objects.get_or_None(user=user)
        contact_form = ContactForm(instance=contact)
        order = Record.objects.get_amount_list(user=user)
    context = {
        'contact_form': contact_form,
        'order': order,
    } 
    return render(request, template, context)
