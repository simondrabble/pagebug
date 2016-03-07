from django.contrib.gis.geos import Point
from django.core import paginator
from django.test import TestCase

from . import models


class PagedModelTest(TestCase):

    def setUp(self):
        super(PagedModelTest, self).setUp()
        models.PagedModel.objects.create(name='Test 1')

    def test_pagination(self):
        point = Point(-101.214, 36.135, srid=4326)

        qs = models.PagedModel.objects.all()
        # Both of these modifiers are required to trigger the bug.
        qs = qs.distance(point)
        qs = qs.extra(select={'confidence': '0'})

        # The '0' above shows up as the column name in a generated group by
        # clause:
        '''
        SELECT COUNT(*) FROM (
          SELECT (0) AS "confidence",
          "example_pagedmodel"."id" AS Col1,
          (ST_distance_sphere("example_pagedmodel"."location",
           ST_GeomFromEWKB('\x0101000020e610000004560e2db24d59c0e17a14ae47114240'::bytea))
          ) AS "distance"
          FROM "example_pagedmodel"

          GROUP BY "example_pagedmodel"."id",
                   (0),    -- Here is the problem
                           -- Should be a 1-based column number,
                           -- or the name of the column ("confidence")

          (ST_distance_sphere("example_pagedmodel"."location",
           ST_GeomFromEWKB('\x0101000020e610000004560e2db24d59c0e17a14ae47114240'::bytea)))
          ) subquery
        '''

        ps = 100
        p = 1

        pager = paginator.Paginator(qs, ps)

        results = pager.page(1)
        self.assertEqual(1, len(results))
