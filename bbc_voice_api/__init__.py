from pyramid.config import Configurator
from pyramid.events import NewRequest

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_subscriber(add_headers_response_callback, NewRequest)
    config.add_route('news', '/news')
    config.add_route('news-topics', '/news/topics')
    config.add_route('weather', '/weather')
    config.add_route('location', '/location')
    config.scan()
    return config.make_wsgi_app()


def add_headers_response_callback(event):
    def headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*'
        })
        response.headers.update({
            'Cache-Control': 'public, max-age=300'
        })
    event.request.add_response_callback(headers)

