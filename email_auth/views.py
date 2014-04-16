# -*- coding=utf8 -*-

import os

from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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

