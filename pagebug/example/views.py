from django import http
from django.contrib.gis.geos import Point
from django.core import paginator
from django.shortcuts import render

from . import models


def index_view(request, *args, **kwargs):
    point = Point(-101.214, 36.135, srid=4326)

    qs = models.PagedModel.objects.all()
    qs = qs.distance(point)
    qs = qs.extra(select={'confidence': '0'})

    ps = 100
    p = 1

    pager = paginator.Paginator(qs, ps)

    try:
        results = pager.page(p)

    except paginator.PageNotAnInteger as e:
        results = pager.page(1)

    except paginator.EmptyPage as e:
        results = pager.page(pager.num_pages)

    return http.HttpResponse()
