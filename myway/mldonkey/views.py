#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db

mldonkeyview = Blueprint('mldonkey', __name__)

