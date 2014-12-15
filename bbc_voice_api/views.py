from pyramid.view import view_config

@view_config(route_name='language-parse', renderer='json')
def language_parse(request):
    return {'project': 'newshack'}
