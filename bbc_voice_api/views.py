from pyramid.view import view_config

@view_config(route_name='news', renderer='json')
def language_parse(request):
    return {'project': 'newshack'}
