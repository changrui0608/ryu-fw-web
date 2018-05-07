import sys
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings as django_settings
from django import forms
from django.urls import reverse
import api


# index page

def index(request):
    return render(request, 'index.html', {})


#  status and settings

def status(request):
    """
    show status of all SWs
    """
    status = api.get_fw_status()
    return render(request, 'status.html', {'status': status})


def status_enable(request, sw='all'):
    """
    enable fw on SWs
    """
    api.enable_fw(sw=sw)
    return HttpResponseRedirect(reverse('status'))


def status_disable(request, sw='all'):
    """
    disable fw on SWs
    """
    api.disable_fw(sw=sw)
    return HttpResponseRedirect(reverse('status'))


# detailed rules

def rules(request, sw_id='all'):
    """
    show all rules in a table
    provide form to add rule
    """
    return render(request, 'default.html')


def rules_add(request):
    """
    add detailed rule
    """
    pass


def rules_delete(request, rule_id='all'):
    """
    delete a rule
    """
    pass


# quick entry for IP based rules

def ip_rules(request):
    """
    (maybe) show rules in a table
    provide form to add IP based rule
    """
    return render(request, 'default.html', {})


def ip_rule_add(request):
    """
    add IP based rule
    """
    pass


def ip_rule_delete(request):
    """
    delete IP based rule
    """
    pass
