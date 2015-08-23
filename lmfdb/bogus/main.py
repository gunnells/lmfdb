# -*- coding: utf-8 -*-
# This Blueprint is about Bogus

from flask import render_template, request, url_for, make_response, redirect
import lmfdb.base
from lmfdb.base import app
from lmfdb.bogus import bogus_page, logger
from lmfdb.utils import to_dict
from pymongo import ASCENDING, DESCENDING
import os
import StringIO
import re

def get_bread(breads=[]):
    bc = [("Bogus", url_for(".index"))]
    for b in breads:
        bc.append(b)
    return bc


bogusdb = None

def db_bogus():
    global bogusdb
    if bogusdb is None:
        bogusdb = lmfdb.base.getDBConnection().bogus.animals
    return bogusdb

def bogus_search(**args):
    info = to_dict(args)
    bread = [('Bogus', url_for("bogus.index")),
             ('Search Results', '.')]
    query = {}

    if info.get('common'):
        pattern = info['common']
        regx = re.compile(pattern, re.IGNORECASE)
        query = {'common': regx }
        cursor = db_bogus().find(query).sort('name',ASCENDING)
        res = cursor
        nres = cursor.count()
        info['nres'] = nres
        info['results'] = cursor
        if nres == 1:
            info['report'] = 'unique match'
        elif nres == 2:
            info['report'] = 'displaying both matches'
        else:
            info['report'] = 'displaying all %s matches' % nres
            
    title = 'Bogus search results'
    credit = 'nobody@nowhere.com'
    if nres == 0:
        info['err'] = 'There was a search error.  No results were found.  Hopefully this helpful message helps.'
        return search_input_error(info, bread, credit)
    
    return render_template("bogus.html", info=info, credit=credit, bread=bread, title=title)


def search_input_error(info, bread, credit):
    return render_template("bogus.html", info=info, credit=credit, bread=bread, title='Bogus Search Input Error')

 
@bogus_page.route("/<common>/")
def by_common(common):
    return bogus_search(common=common, **request.args)



# @bogus_page.route("/<bogus>", methods=["GET"])
# def show(bogus):
#     C = make_tableaux_bogus(bogus)
#     bc = get_bread([(bogus, url_for('.show', bogus=bogus))])
#     return render_template("bogus.html", bogus=C, bogus_string=bogus, bread=bc)


@bogus_page.route("/search")
def search():
    weight = request.args.get('weight', '')
    weight = weight.replace(',', '.')
    cartan_type = str(request.args.get('cartan_type', ''))
    rank = request.args.get('rank', '')
    logger.info("weight = %s" % weight)
    if not (cartan_type and rank and weight):
        return redirect(url_for('.index'))
    bogus_string = "-".join([cartan_type, rank, weight])
    return redirect(url_for('.show', bogus=bogus_string))

@bogus_page.route("/")
def index():
    bread = get_bread()
    return render_template("bogus-index.html", title="Bogus", bread=bread)
