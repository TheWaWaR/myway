#!/usr/bin/env python
#coding=utf-8

import os
import pickle
import time
from datetime import datetime, timedelta
import pytz
from multiprocessing import Process
from flask import Blueprint, request
from weibo import APIClient

moduleid = 'weibo'
weiboview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

APP_KEY = '781743531'
APP_SECRET = '90849f6986665f841090d2e245e9f31c'
CALLBACK_URL = 'http://ahorn.me/weibo/callback'
TOKENS_FILE = 'tokens'
QUEUE_FILE = 'queue'
PROCESS_STARTED = False

MESSAGES = [u'Good day!',
        u'If you try something again and again and again, one day you\'ll get over it, the delightful sense is worth to fight!',
        u'Happy day, boys!']



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


def sleep_util_next_day():
    IT = pytz.timezone('Asia/Shanghai')
    dt_day = timedelta(1)
    cn_now = datetime.now(IT)
    next_day = cn_now + dt_day
    next_cn_now = datetime(next_day.year, next_day.month, next_day.day, 2, 0, 0, 0, IT)
    d_secs = int((next_cn_now - cn_now).total_seconds())
    time.sleep(d_secs)

def check_queue_OK():
    is_OK = True
    if os.path.isfile(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            l = f.readline()
            if l.startswith('STOP'):
                is_OK = False
    return is_OK

def update_private_statues():
    count = 0
    while True:
        if not check_queue_OK():
            return
        try:
            input_file = open(TOKENS_FILE, 'rb')
            tokens = pickle.load(input_file)
            input_file.close()
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            status_ids = []
            for t in tokens:
                print 'Update for %s, <%d>' % (str(t.uid), count)
                client.set_access_token(t.access_token, t.expires_in)
                for i in range(5):
                    status_ret = client.statuses.update.post(status=u'Test private update ' + str(i)*5, visible=2)
                    status_ids.append(status_ret.id)
                    for j in range(10):
                        client.comments.create.post(comment=u'Good post ' + str(j)*5, id=status_ret.id)
                    time.sleep(5)
                client.statuses.update.post(status=MESSAGES[count%len(MESSAGES)], visible=2)
            time.sleep(60)
            for sid in status_ids:
                client.statuses.destroy.post(sid)
            count += 1
            sleep_util_next_day()
        except IOError:
            time.sleep(60)
            print 'No token'


def start_process():
    p = Process(target=update_private_statues, args=())
    p.start()


# ==============================================================================
#  Views
# ==============================================================================
@weiboview.route('/')
def register():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return u'''<a href="%s">%s</a>''' % (url, url)

@weiboview.route('/start')
def start():
    global PROCESS_STARTED
    if not PROCESS_STARTED:
        start_process()
        PROCESS_STARTED = True
    return 'OK'


@weiboview.route('/stop')
def stop():
    with open(QUEUE_FILE, 'w') as f:
        f.write('STOP')
    return 'OK'

@weiboview.route('/callback')
def callback():
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
    return 'OK'
