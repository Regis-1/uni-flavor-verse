from flask import Blueprint

bp_skladniki = Blueprint('skladniki', __name__)

from . import page
