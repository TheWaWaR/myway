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
