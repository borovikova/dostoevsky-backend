import re

import pandas as pd

from app.constants import UNCOUNTABLE
from part.models import Part


def prepare_query_params(query_params):
	year = query_params.get('year')
	if year:
		year = year.split(',')

	part = query_params.get('part')
	if part:
		part = part.split(',')

	params = query_params.get('param')
	params = params.split(',') if params else []
	params = [_ for _ in params if _ != 'name']

	breakdowns = query_params.get('breakdowns')
	breakdowns = breakdowns.split(',') if breakdowns else []

	return year, part, params, breakdowns


def add_filters_to_response(year, part, params, breakdowns, ret):
	if len(breakdowns) < 2:
		if 'year' not in ret:
			uncount = {param: None for param in params if param in UNCOUNTABLE}
			if uncount:
				ret.update(uncount)
			if len(year) > 1:
				years = [int(_) for _ in year]
				ret['year'] = '-'.join([str(min(years)), str(max(years))])
			else:
				ret['year'] = str(year[0])
		if 'part' not in ret:
			uncount = {param: None for param in params if param in UNCOUNTABLE}
			if uncount:
				ret.update(uncount)
			ret['part'] = ', '.join(sorted(part)) if len(part) > 1 else part[0]
	return ret


def get_clause(part):
	if re.search(r'[Вв]оинск', part):
		return "Воинские преступления"
	return re.search(r'(\d{3}(\.\d{1}|))', part).group()


def get_all_filters():
	df = pd.DataFrame(Part.objects.order_by('part').values())

	parts = df.drop_duplicates(subset=['part'])['part'].values.tolist()
	clauses = sorted(list(set([get_clause(part) for part in parts])))
	years = df.drop_duplicates(subset=['year'])['year'].values.tolist()
	categories = df.drop_duplicates(subset=['category']).dropna()['category'].values.tolist()

	df.loc[:, 'params'] = df.apply(lambda row: list(row.parameters.keys()), axis=1)
	df = df.explode('params')
	params = sorted(df.drop_duplicates(subset=['params'])['params'].values.tolist())

	return {
		"clause": sorted(clauses),
		"part": sorted(parts),
		"year": sorted(years),
		"category": sorted(categories),
		"parameters": sorted(params)
	}
