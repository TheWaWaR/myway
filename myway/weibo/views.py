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
    count = 0
    while True:
        try:
            input_file = open(TOKENS_FILE, 'rb')
            tokens = pickle.load(input_file)
            input_file.close()
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            for t in tokens:
                print 'Update for %s, <%d>' % (str(t.uid), count)
                client.set_access_token(t.access_token, t.expires_in)
                for i in range(3):
                    client.statuses.update.post(status=u'Test private update ' + str(i)*6, visible=2)
                    time.sleep(5)
            count += 1
            time.sleep(3600*23.5)
        except IOError:
            time.sleep(60)
            print 'No token'


def start_process():
    p = Process(target=update_private_statues, args=())
    p.start()

# ==============================================================================
#  Views
# ==============================================================================
@weiboview.route('/weibo/')
def weibo():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return u'''<a href="%s">%s</a>''' % (url, url)

@weiboview.route('/weibo/start')
def weibo():
    global PROCESS_STARTED
    if not PROCESS_STARTED:
        start_process()
        PROCESS_STARTED = True
    return 'OK'

@weiboview.route('/weibo/callback')
def weibo_callback():
    code = request.args.get('code', '')
    print code
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    t = client.request_access_token(code)
    access_token = t.access_token # 新浪返回的token，类似abc123xyz456
    expires_in = t.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4

    # TODO: 在此可保存access token
    client.set_access_token(access_token, expires_in)
    # print client.statuses.update.post(status=u'测试OAuth 2.0发微博')

    save_token(t)
    global PROCESS_STARTED
    if not PROCESS_STARTED:
        start_process()
        PROCESS_STARTED = True
    return 'OK'
