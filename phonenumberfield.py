# -*- coding=utf8 -*-

from django import forms
from django.db import models
from django.core.validators import RegexValidator 


class CellphoneInput(forms.widgets.TextInput):
    input_type = 'tel'


class CellphoneFormField(forms.CharField):
    widget = CellphoneInput

    def __init__(self, pattern=None,  *args, **kwargs):
        self.pattern = pattern
        forms.CharField.__init__(self, *args, **kwargs)
        if pattern is not None:
            self.validators.append(RegexValidator(regex=self.pattern,
                message=u'請輸入手機號碼',code=u'invalid phone number'))

    def widget_attrs(self, widget):
        attrs = super(CellphoneFormField, self).widget_attrs(widget)
        if self.pattern is not None and isinstance(widget, CellphoneInput):
            attrs.update({'pattern': str(self.pattern)})
        return attrs


class CellphoneModelField(models.CharField):
    description = u"Cell Phone Number"

    def __init__(self, pattern=None, *args, **kwargs):
        models.CharField.__init__(self, *args, **kwargs)
        self.pattern = pattern
        self.validators.append(RegexValidator(regex=self.pattern,
            message=u'請輸入手機號碼',code=u'invalid phone number'))

    def get_internal_type(self):
        return "CellphoneModelField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CellphoneFormField,
            'pattern': self.pattern,
        }
        defaults.update(kwargs)
        return super(CellphoneModelField, self).formfield(**defaults)
