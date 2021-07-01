import json

import pytest
import yaml
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from part.models import Part
from part.serializers import PartSerializer
from part.utils import get_all_filters


@pytest.mark.snapshot
@pytest.mark.django_db
def test_full_data_view(snapshot):
	data = sorted(PartSerializer(Part.objects.all(), many=True).data, key=lambda item: (item["part"], item["year"]))
	for d in data:
		del d["id"]
	snapshot.assert_match(JSONRenderer().render(data), 'full_data.json')


@pytest.mark.snapshot
@pytest.mark.django_db
def test_all_parameters_view(snapshot):
	client = APIClient()
	user = get_user_model().objects.create_user(
		'test@test.com',
		'testpass'
	)
	client.force_authenticate(user)

	url = reverse('part:filters-list')
	res = client.get(url)
	snapshot.assert_match(yaml.dump(json.loads(res.content)), 'all_parameters.yml')


def request_with_test_client(year, param, part, breakdowns):
	client = APIClient()
	user = get_user_model().objects.create_user(
		'test@test.com',
		'testpass'
	)
	client.force_authenticate(user)
	url = reverse('part:aggregated_data')
	payload = {
		"year": year,
		"param": param,
		"part": part,
		"breakdowns": breakdowns
	}
	return client.post(url, json.dumps(payload), content_type='application/json')


@pytest.mark.snapshot
@pytest.mark.django_db
@pytest.mark.parametrize("breakdowns", [[], ['part'], ['year'], ['part', 'year']])
@pytest.mark.parametrize("year, param, part", [
	([2020], ["totalConvicted"], ["105ч.1"]),
	([2020, 2019, 2012, 2009], ["totalConvicted"], ["105ч.1"]),
	([2020, 2019, 2012, 2009], ["totalConvicted", "primaryForcedLabour", "addFineSum", "corruption"], ["105ч.1"]),
	([2020, 2019, 2012, 2009],
	 ["totalConvicted", "primaryForcedLabour", "addFineSum", "corruption"],
	 ["105ч.1", "118", "196", "322.3"]),
])
def test_aggregated_data_view(snapshot, year, param, part, breakdowns):
	res = request_with_test_client(year, param, part, breakdowns)
	snapshot.assert_match(yaml.dump(json.loads(res.content)),
	                      f'year_{len(year)}_params_{len(param)}_clause_{len(part)}_breakdowns_{len(breakdowns)}.yml')


@pytest.mark.snapshot
@pytest.mark.django_db
@pytest.mark.parametrize("breakdowns", [[], ['part'], ['year'], ['part', 'year']])
def test_full_aggregated_data(snapshot, breakdowns):
	filters = get_all_filters()
	year = filters.get('year', [])
	param = filters.get('parameters', [])
	part = filters.get('part', [])

	res = request_with_test_client(year, param, part, breakdowns)
	snapshot.assert_match(yaml.dump(json.loads(res.content)),
	                      f'year_{len(year)}_params_{len(param)}_clause_{len(part)}_breakdowns_{len(breakdowns)}.yml')
