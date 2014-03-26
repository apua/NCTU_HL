# -*- coding=utf8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shopping_cart.models import Product, Record, Contact, ContactForm

@login_required(login_url='/login/')
def order(request):

    if request.method=='POST':
        return HttpResponse(">//////<")

    else:
        user = request.user
        contact = Contact.objects.get_or_None(user=user)
        order = Product.objects.get_amount_list(model=Record, user=user)
        context = {
            'order': order,#.order_by('id'),
            'contact_form': ContactForm(instance=contact),
        }
        return render(request, 'shopping_cart/order_form.html', context)
