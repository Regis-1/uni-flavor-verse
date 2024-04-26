from flask import Blueprint

bp_przepisy = Blueprint('przepisy', __name__)

from . import page
