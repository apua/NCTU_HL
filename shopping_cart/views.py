# -*- coding=utf8 -*-


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def list_product(request):
    return HttpResponse('list_product')


@login_required(login_url='/signup/')
def order(request):
    return HttpResponse('order')


def signup(request):
    return HttpResponse('signup')
