#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  quantpy
@file:    utils.py
@time:    2018/4/13 15:46
"""
import inspect
import smtplib
from email.mime.text import MIMEText


def get_full_parameters(func, *args, **kwargs):
    """
    get full function parameters by
    given parameter and default parameter
    """
    sig = inspect.signature(func)
    sig_bind = sig.bind(*args, **kwargs)
    sig_bind.apply_defaults()
    return sig_bind.args, sig_bind.kwargs, sig_bind


def send_email(server_info, sender_info, receivers, subject, content):
    msg = MIMEText(repr(content), 'plain', 'utf8')
    msg['From'] = sender_info.get('from', sender_info['address'])
    msg['Subject'] = subject
    try:
        smtp = smtplib.SMTP(server_info['host'], server_info.get('port', 25))
        smtp.login(sender_info['address'], sender_info['password'])
        smtp.sendmail(sender_info['address'], receivers, msg.as_string())
    except smtplib.SMTPException as e:
        print(e)

