#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from random import Random

from flask_sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, IMAGES

db = SQLAlchemy()

images = UploadSet("images", IMAGES)
rand = Random(datetime.now())

# ==============================================================================
#  Login
# ==============================================================================
from myway.common.login import LoginManager
from myway.common.models import User

login_mgr = LoginManager()
login_mgr.login_view = "/login"
login_mgr.login_message = 'Permission denied!'
login_mgr.refresh_view = "/reauth"

@login_mgr.user_loader
def load_user(id):
    return User.query.get(int(id))
    
# ==============================================================================
#  Navbar
# ==============================================================================
# coding: utf-8

from jinja2 import Markup

class Navbar(object):
    
    def __init__(self):
        self.navs = []

    def __iter__(self):
        return iter(self.navs)

    def __len__(self):
        return len(self.navs)

    def add(self, name, title, href):
        self.navs.append(Nav(name, title, href))

class Nav(object):
    
    def __init__(self, name, title, href):
        self.name = name
        self.title = title
        self.href = href

    def render(self, active = None):
        css_cls = 'active' if active == self.name else ''
        return Markup('<li id="menu-%s" class="%s"><a href="%s">%s</a></li>'
                      % (self.name, css_cls, self.href, self.title))

    def __repr__(self):
        return "Nav(name = %s, title = %s, href = %s)" % (self.name, self.title, self.href)

navbar = Navbar()

# ==============================================================================
#  Markdown parser
# ==============================================================================
import misaka 
from misaka import HtmlRenderer, SmartyPants
from xml.sax.saxutils import escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Create a custom renderer
class BleepRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % escape(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

# And use the renderer
renderer = BleepRenderer()
md = misaka.Markdown(renderer,
        extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)

# print md.render('Some Markdown text.')
