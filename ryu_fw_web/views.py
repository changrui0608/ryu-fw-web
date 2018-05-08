import sys

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings as django_settings
from django import forms
from django.urls import reverse

import api
from .forms import RuleForm, IPAddrRuleForm, SimplifiedRuleForm
from rules import ALLOW_RULES, DENY_RULES
from . import utils


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
    rules = utils.flatten_rules(api.get_rules(sw=sw_id))
    form = RuleForm()
    return render(request, 'rules.html', {'rules': rules, 'form': form})


def rules_add(request):
    """
    add detailed rule
    """
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            rule_data = { k: v for k, v in form.cleaned_data.items() if v }
            api.add_rule(**rule_data)
            return HttpResponseRedirect(reverse('rules'))
    else:
        form = RuleForm()
    return render(request, 'add_rule.html', {'form': form})


def rules_delete(request, rule_id='all'):
    """
    delete a rule
    """
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            api.delete_rule(rule_id=rule_id)
            return HttpResponseRedirect(reverse('rules'))
    else:
        return HttpResponseRedirect(reverse('rules'))

# shortcut for global rules

def rules_allow_all(request):
    """
    Remove all current rules,
    and add a rule that allow all traffics with priority = 0
    """
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            api.delete_rule()
            for rule in ALLOW_RULES:
                api.add_rule(**rule)
            return HttpResponseRedirect(reverse('rules'))
    else:
        return HttpResponseRedirect(reverse('rules'))
        

def rules_deny_all(request):
    """
    Remove all current rules,
    and add a rule that deny all traffics with priority = 0
    """
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            api.delete_rule()
            for rule in DENY_RULES:
                api.add_rule(**rule)
            return HttpResponseRedirect(reverse('rules'))
    else:
        return HttpResponseRedirect(reverse('rules'))


# quick entry for IP based rules

def ip_rules(request):
    """
    (maybe) show rules in a table
    provide form to add IP based rule
    """
    rules = api.get_rules()
    rules = utils.flatten_rules(rules)
    rules = utils.filter_pure_ip_rules(rules)
    form = IPAddrRuleForm()
    return render(request, 'ip_rules.html', {'rules': rules, 'form': form})


def ip_rules_add(request):
    """
    add IP based rule
    """
    if request.method == 'POST':
        form = IPAddrRuleForm(request.POST)
        if form.is_valid():
            rule_data = { k: v for k, v in form.cleaned_data.items() if v }
            api.add_rule(**rule_data)
            return HttpResponseRedirect(reverse('ip_rules'))
    else:
        return HttpResponseRedirect(reverse('ip_rules'))

def ip_rules_delete(request, rule_id):
    """
    delete a rule and redirect to 'ip_rules'
    """
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            api.delete_rule(rule_id=rule_id)
            return HttpResponseRedirect(reverse('rules'))
    else:
        return HttpResponseRedirect(reverse('ip_rules'))
