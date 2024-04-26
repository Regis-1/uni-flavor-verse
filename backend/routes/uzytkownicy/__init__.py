from flask import Blueprint

bp_uzytkownicy = Blueprint('uzytkownicy', __name__)

from . import page
