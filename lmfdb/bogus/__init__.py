# -*- coding: utf-8 -*-
from lmfdb.base import app
from lmfdb.utils import make_logger
from flask import Blueprint

bogus_page = Blueprint("bogus", __name__, template_folder='templates', static_folder="static")
logger = make_logger(bogus_page)


@bogus_page.context_processor
def body_class():
    return {'body_class': 'Bogus'}

import main

app.register_blueprint(bogus_page, url_prefix="/Bogus")
