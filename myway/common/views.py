#!/usr/bin/env python
#coding=utf-8

import os

from flask import Blueprint, render_template, request,\
	 redirect, url_for, flash, json
from myway.utils import db
from myway.blog.models import Article
from .models import User
from .forms import LoginForm
from .login import login_user, logout_user

moduleid = 'common'
commonview = Blueprint(moduleid, __name__)


@commonview.route('/')
def layout():
    return redirect(url_for('blog.index'))

@commonview.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(next=request.args.get('next', ''))
    if form.is_submitted and form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        next = form.next.data
        user, authenticated =  User.authenticate(login, password)
        if user and authenticated:
            login_user(user, remember=True)
            flash('Log in successed!', 'success')
            if next:
                return redirect(next)
            return redirect('/blog/')
        flash('Username or password is wrong!', 'error')
    return render_template('common/login.html', form=form)

    
@commonview.route('/logout')
def logout():
    logout_user()
    flash('Log out successed!', 'success')
    return redirect('/blog/')
    
# ==============================================================================
#  Topo
# ==============================================================================
@commonview.route('/topo-private')
def topo():
    return render_template('common/topo.html')

@commonview.route('/topo/directory.json')
def json_load_directory():
    spath = request.args.get('path', '')
    data = None
    lvs_all = ['ROOT', 'STAR', 'COUNTRY', 'PROVINCE', 'CITY']
    
    if spath:
        data = []
        path = spath.split(',')
        if len(path) >= len(lvs_all):
            return json.dumps([])
        lvs = [i.split('-')[0].upper() for i in path]
        lv = lvs_all[len(lvs)]
        for i in range(1, 8):
            node = {
                'name'     : '%s-%s' % (lv ,str(i)),
                'children' : None,
                'level'    : len(lvs)-1,
                'id'       : '%s-%s' % (lv.lower() ,str(i)),
            }
            node['_children'] = [] if  (len(path) < len(lvs_all)-1) else None
            data.append(node)
    else:
        data = {
            'name'     : 'ROOT-0',
            'children' : [],
            'level'    : 0,
            'id'       : 'root-0',
        }
        for i in range(1, 100):
            node = {
                'name'     : 'STAR-' + str(i),
                'children' : [],
                'level'    : 1,
                'id'       : 'star-' + str(i)
            }
            data['children'].append(node)
    return json.dumps(data)
    
@commonview.route('/topo/nodes.json')
def json_load_nodes():
    # 1. 缩放           DONE
    # 2. 拖拽           DONE
    # 3. 链接           DONE
    # 4. 显示图片       DONE
    # 5. 表达节点的状态 DONE
    # 6. 右键菜单       DONE
    # 7. 搜索跳转       DONE
    from random import Random
    rand = Random()
    
    spath = request.args.get('path', 'star-0')
    na    = request.args.get('na', 7, type=int)
    nb    = request.args.get('nb', 7, type=int)
    nnc   = request.args.get('nc', 7, type=int)

    ca = cb = cc = 0;
    country_lv, province_lv, city_lv = 2, 3, 4
    path = spath.split(',')[1:]
    lvs = [i.split('-')[0].upper() for i in path]
    
    data = {
        'name'     : path[0].upper(),
        'children' : [],
        'level'    : 1,
        'maxlevel' : 1,
        'maxpath'  : len(path) - 1,
        'id'       : path[0]
    }

    def selected(s, i):
        if s in lvs and '%s-%d' % (s.lower(), i) not in path:
            return False
        return True
    print '========================================'
    print spath, path, lvs
    print '--------------------'
    
    for a in range(na):         # COUNTRY
        ca = a+1
        A = {'name': 'COUNTRY-' + str(ca), 'children': [],
             'level': country_lv, 'id': 'country-'+str(ca), "size": ca * 30}
        for b in range(nb):     # PROVINCE
            cb = b+1
            B = {'name': 'PROVINCE-' + str(cb), 'children': [],
                 'level': province_lv, 'id': 'province-'+str(cb), "size": cb * 30}
            nc = nnc
            for c in range(nc): # CITY
                cc = c+1
                C = {'name': 'CITY-' + str(cc), 'url': 'http://www.stackoverflow.com',
                     'level': city_lv, 'id': 'city-'+str(cc) , "size": cc * 30}
                C['status'] = 1 if c % rand.randint(2, 6) != 0 else 0
                C['lstatus'] =  1 if c % 5 > 1 else 0
                if selected('CITY', cc):
                    if data['maxlevel'] < city_lv:
                        data['maxlevel'] = city_lv;
                    B['children'].append(C)
            if selected('PROVINCE', cb):
                if data['maxlevel'] < province_lv:
                    data['maxlevel'] = province_lv;
                A['children'].append(B)
        if selected('COUNTRY', ca):
            if data['maxlevel'] < country_lv:
                data['maxlevel'] = country_lv;
            data['children'].append(A)

    def pdict(d):
        print d['id'],
        if 'children' in d:
            print len(d['children'])
            for c in d['children']:
                pdict(c)
    # pdict(data)
    return json.dumps(data)


