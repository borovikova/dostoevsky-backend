from app.constants import UNCOUNTABLE

def prepare_query_params(query_params):
    year = query_params.get('year')
    if year:
        year = year.split(',')

    part = query_params.get('part')
    if part:
        part = part.split(',')

    category = query_params.get('category')
    if category:
        category = category.split(',')

    params = query_params.get('param')
    params = params.split(',') if params else []

    breakdowns = query_params.get('breakdowns')
    breakdowns = breakdowns.split(',') if breakdowns else []

    return year, part, category, params, breakdowns

def add_filters_to_response(query_params, ret):
    year, part, category, params, breakdowns = prepare_query_params(query_params)
    if len(breakdowns) < 2:
        if 'part' in breakdowns or len(breakdowns) == 0:
            ret.update({param: None for param in params if param in UNCOUNTABLE})
            if len(year) > 1:
                years = [int(_) for _ in year]
                ret['year'] = '-'.join([str(min(years)), str(max(years))])
            else:
                ret['year'] = year[0]
        if 'year' in breakdowns or len(breakdowns) == 0:
            ret.update({param: None for param in params if param in UNCOUNTABLE})
            ret['part'] = ', '.join(sorted(part)) if len(part) > 1 else part[0]
    return ret

