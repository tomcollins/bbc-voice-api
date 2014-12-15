from pyramid.config import Configurator
from pyramid.events import NewRequest

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    config.add_route('news', '/news')
    config.add_route('weather', '/weather')
    config.scan()
    return config.make_wsgi_app()


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*'
        })
    event.request.add_response_callback(cors_headers)

