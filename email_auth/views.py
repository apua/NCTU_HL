# -*- coding=utf8 -*-

import os

from django import forms
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.translation import ugettext, ugettext_lazy as _

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from models import User


def backup_database():
    try:
        from django.conf import settings
        import shutil, datetime
        src = settings.DATABASES['default']['NAME']
        dst = src + '_' + str(datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
        shutil.copy(src, dst)
        return True
    except:
        return False


@transaction.atomic
@login_required(login_url='/login/')
@csrf_exempt
def clean_database(request):

    if not request.user.is_superuser:
        return HttpResponse('only staff user can run cleaning process')
    elif not request.user.is_staff:
        return HttpResponse('Why R U fxxking here A___Aa?? There should not be any staff user without super permission')

    if request.POST:
        # backup db
        backup_successfully = backup_database()
        #if not backup_successfully:
        #    return HttpResponse(u'wooops....backup failed')

        # remove all contacts, records, users
        # except superusers
        # products and information would not be modified
        from shopping_cart.models import Record, Contact
        from email_auth.models import User
        Record._default_manager.all().delete()
        Contact._default_manager.all().delete()
        User._default_manager.exclude(is_staff=True).delete()
        return HttpResponse(u'已清除資料')

    # list what would be clean
    return HttpResponse(u'將刪除所有 records, contacts, users, 除了 superuser'\
        '<form method="POST"><input name="a"><input type="submit"></form>')


class SignupForm(forms.Form):
    email = forms.fields_for_model(User)['email']
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_email(self):
        '''check if account (email) exists'''
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(u'此帳號已存在', code='email_exists')
        return self.cleaned_data['email']

    def clean_password2(self):
        '''compare passwords'''
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(
                _("The two password fields didn't match."),
                code='password_mismatch',
            )
        return self.cleaned_data['password2']

    def save(self, request, template='registration/signup_email.html'):
        '''save user model and send email'''
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        # save user model
        user = User.objects.create_nonregistered_user(email=email, password=password)
        # send email
        from django.core.mail import send_mail
        from django.template import loader
        from django.contrib.sites.models import get_current_site
        mail_from = User.objects.filter(is_superuser=True).first().email
        rcpt_to = email
        subject = u'洄瀾週帳號開通'
        mail_content = loader.render_to_string(template, {
            'email': user.email,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        send_mail(subject, mail_content, mail_from, (rcpt_to,))


@sensitive_post_parameters()
@never_cache
def signup(request, template='registration/signup_form.html'):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            # save user model and send email
            form.save(request)
            return HttpResponseRedirect(reverse('signup_done'))
    else:
        form = SignupForm()
    #return HttpResponse(u'帳號申請')
    return render(request, template, {'form':form})


def signup_done(request):
    return HttpResponse(u'確認信已寄出 (待認證)')


def signup_confirm(request, uidb64=None, token=None):
    '''according "uidb64" and "token" to set user active'''
    # there should be only GET method
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except:
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(u'帳號成功開通 (redirect to order page)')
    else:
        return HttpResponse(u'連結失效')
