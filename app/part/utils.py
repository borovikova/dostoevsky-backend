from app.constants import UNCOUNTABLE

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

