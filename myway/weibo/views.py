#!/usr/bin/env python
#coding=utf-8

import os
import pickle
import time
import random
from datetime import datetime, timedelta
import pytz
from multiprocessing import Process
from flask import Blueprint, request
from weibo import APIClient, APIError

moduleid = 'weibo'
weiboview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

APP_KEY = '781743531'
APP_SECRET = '90849f6986665f841090d2e245e9f31c'
CALLBACK_URL = 'http://ahorn.me/weibo/callback'

POMES_FILE = 'FeiNiaoJi.txt'
TOKENS_FILE = 'tokens'
QUEUE_FILE = 'queue'
MARK = '>>>[WEIBO] '
PROCESS_STARTED = False
PROCESS_POOL = {}

def load_messages():
    poems = None
    with open(POMES_FILE, 'rb') as f:
        poems = pickle.load(f)
    return poems


def save_token(nt):
    tokens = []
    try:
        input_file = open(TOKENS_FILE, 'rb')
        tokens = pickle.load(input_file)
        input_file.close()
    except IOError:
        print MARK + 'INIT tokens file'

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
    print MARK + 'SLEEP <%d> minutes.' % (d_secs/60, )
    time.sleep(d_secs)
    print MARK + 'WEAK UP'

def check_queue_OK():
    is_OK = True
    return is_OK  # !!! For test !!!
    if os.path.isfile(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            l = f.readline()
            if l.startswith('STOP'):
                is_OK = False
    return is_OK

def post_status(client, cont, visb):
    status_ret = None
    try:
        status_ret = client.statuses.update.post(status=cont, visible=visb)
    except APIError, e:
        print MARK + "(status): ", e
    except Exception, e:
        print MARK + "OTHER Exception(status): ", e
    return status_ret


def post_comment(client, cont, sid):
    cmt_ret = None
    try:
        cmt_ret = client.comments.create.post(comment=cont, id=sid)
    except APIError, e:
        print MARK + "(comment): ", e
    except Exception, e:
        print MARK + "OTHER Exception(comment): ", e
    return cmt_ret


def get_poem(poems, count):
    poem = poems[count%len(poems)]
    num_title = poem['num_title']
    content = poem['content']
    return '%s. %s' % (num_title, content)

def do_task(client, t, poems, count):
    '''Do post statuses task then return the new count'''
    r = random.Random()
    status_ids = []
    print MARK + 'Update for user <%s>, count <%d>' % (str(t.uid), count)
    client.set_access_token(t.access_token, t.expires_in)
    for i in range(6):
        status_ret = post_status(client, get_poem(poems, count) , 2)
        count += 1
        if status_ret is None:
            continue
        status_ids.append(status_ret.id)
        for j in range(9):
            time.sleep(5)
            cmt_ret = post_comment(client, 'Good day, <%d>.' % (r.randint(0, 100) + j*100), status_ret.id)
            if cmt_ret is None:
                continue
        time.sleep(3)
    print MARK + 'POSTED ids: %r' % status_ids
    return count


def update_private_statues(wait):
    count = 0
    poems = load_messages()
    if wait == 'YES':
        sleep_util_next_day()

    while True:
        if not check_queue_OK():
            print MARK + '<STOP> SIGNAL from file'
            return
        try:
            try:
                input_file = open(TOKENS_FILE, 'rb')
                tokens = pickle.load(input_file)
                input_file.close()
            except IOError, e:
                print MARK + "No Token: ", e
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            for t in tokens:
                count = do_task(client, t, poems, count)
                time.sleep(3600)

            sleep_util_next_day()
        except IOError, e:
            print MARK + "Network Error?: ", e
            time.sleep(60)


def start_process(wait):
    p = Process(target=update_private_statues, args=(wait,))
    p.daemon = True
    p.start()
    global PROCESS_POOL
    PROCESS_POOL[p.pid] = p
    print MARK + 'Process started <%d>!' % p.pid
    return p


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
    wait = request.args.get('wait', 'YES')
    global PROCESS_STARTED
    p = None
    if not PROCESS_STARTED:
        p = start_process(wait)
        PROCESS_STARTED = True
    ret = p.pid if p else 'None'
    return 'OK, <%r>' % ret


@weiboview.route('/stop')
def stop():
    global PROCESS_POOL, PROCESS_STARTED
    pids = []
    for pid in PROCESS_POOL:
        p = PROCESS_POOL[pid]
        print MARK + "STOP process:" + str(pid)
        pids.append(pid)
        p.terminate()
    PROCESS_POOL = {}
    PROCESS_STARTED = False
    return 'OK, <%r>' % pids


@weiboview.route('/callback')
def callback():
    code = request.args.get('code', '')
    print MARK + 'New CODE: ' + code
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    t = client.request_access_token(code)
    access_token = t.access_token # 新浪返回的token，类似abc123xyz456
    expires_in = t.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4

    # TODO: 在此可保存access token
    client.set_access_token(access_token, expires_in)
    # print MARK + client.statuses.update.post(status=u'测试OAuth 2.0发微博')

    save_token(t)
    return 'OK'

