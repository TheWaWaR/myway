#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, request, redirect, url_for, flash, json
from weibo import APIClient

moduleid = 'weibo'
weiboview = Blueprint(moduleid, __name__)

APP_KEY = '781743531'
APP_SECRET = '90849f6986665f841090d2e245e9f31c'
CALLBACK_URL = 'http://ahorn.me/weibo/callback'


@weiboview.route('/weibo/')
def weibo():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return u'''<a href="%s">%s</a>''' % (url, url)

@weiboview.route('/weibo/callback')
def weibo_callback():
    code = request.args.get('code', '')
    print code
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token # 新浪返回的token，类似abc123xyz456
    expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    # TODO: 在此可保存access token
    client.set_access_token(access_token, expires_in)
    print client.statuses.update.post(status=u'测试OAuth 2.0发微博')
    return client.statuses.user_timeline.get()
