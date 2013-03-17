#!/usr/bin/env python
#coding=utf-8

import pickle
import time
from multiprocessing import Process
from flask import Blueprint, request
from weibo import APIClient

moduleid = 'weibo'
weiboview = Blueprint(moduleid, __name__)

APP_KEY = '781743531'
APP_SECRET = '90849f6986665f841090d2e245e9f31c'
CALLBACK_URL = 'http://ahorn.me/weibo/callback'
TOKENS_FILE = 'tokens'
PROCESS_STARTED = False


def save_token(nt):
    tokens = []
    try:
        input_file = open(TOKENS_FILE, 'rb')
        tokens = pickle.load(input_file)
        input_file.close()
    except IOError:
        print 'INIT tokens file'

    new_token_dict = {}
    for t in tokens + [nt]:
        new_token_dict[t.uid] = t
    new_tokens = new_token_dict.values()
    output_file = open(TOKENS_FILE, 'wb')
    pickle.dump(new_tokens, output_file)
    output_file.close()

def update_private_statues():
    while True:
        try:
            input_file = open(TOKENS_FILE, 'rb')
            tokens = pickle.load(input_file)
            input_file.close()
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            for t in tokens:
                client.set_access_token(t.access_token, t.expires_in)
                for i in range(6):
                    client.statuses.update.post(status=u'Test private update ' + str(i)*6, visible=2)
                    time.sleep(5)
            time.sleep(3600*24)
        except IOError:
            time.sleep(60)
            print 'No token'


def start_process():
    p = Process(target=update_private_statues, args=())
    p.start()
    p.join()

# ==============================================================================
#  Views
# ==============================================================================
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
    # print client.statuses.update.post(status=u'测试OAuth 2.0发微博')

    save_token(r)
    global PROCESS_STARTED
    if not PROCESS_STARTED:
        start_process()
        PROCESS_STARTED = True
    return 'OK'
