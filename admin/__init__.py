from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import SQLDB
admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='logos')
db = SQLDB()

from . import routes