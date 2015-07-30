# -*- coding: utf-8 -*-
# This Blueprint is about Bogus

from flask import render_template, request, url_for, make_response, redirect


def get_bread(breads=[]):
    bc = [("Bogus", url_for(".index"))]
    for b in breads:
        bc.append(b)
    return bc


def make_tableaux_bogus(bogus):
    from sage.all_cmdline import BogusOfTableaux
    cartan, rank, weight = bogus.split("-")
    weight = weight.split(".")
    return BogusOfTableaux([str(cartan), int(rank)], shape=tuple(map(int, weight)))


def make_path_bogus(bogus):
    from sage.all_cmdline import BogusOfLSPaths
    cartan, rank, weight = bogus.split("-")
    weight = weight.split(".")
    return BogusOfLSPaths([str(cartan), int(rank)], map(int, weight))


@bogus_page.route("/<bogus>", methods=["GET"])
def show(bogus):
    C = make_tableaux_bogus(bogus)
    bc = get_bread([(bogus, url_for('.show', bogus=bogus))])
    return render_template("bogus.html", bogus=C, bogus_string=bogus, bread=bc)


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


@bogus_page.route("/search_littelmann")
def search_littelmann():
    weight = request.args.get('weight', '')
    weight = weight.replace(',', '.')
    cartan_type = str(request.args.get('cartan_type', ''))
    logger.info("weight = %s" % weight)
    if not (cartan_type and weight):
        return redirect(url_for('.index'))
    bogus_string = "-".join([cartan_type, str(2), weight])
    return redirect(url_for('.show_littelmann', bogus=bogus_string))

@bogus_page.route("/")
def index():
    bread = get_bread()
    return render_template("bogus-index.html", title="Bogus", bread=bread)
