from flask import Flask, jsonify, Request, Response
import functions_framework
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Request as WerkzeugRequest



def convert_request(request):
    """
    Convert a functions_framework request to a Flask request.
    """
    # Create a new werkzeug environment dictionary
    environ = {
        'REQUEST_METHOD': request.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string.decode('utf-8'),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'CONTENT_TYPE': request.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': request.headers.get('Content-Length', 0),
        'wsgi.url_scheme': request.scheme,
        'wsgi.input': request.data,
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers to the environment
    headers = Headers(request.headers)
    environ.update(headers.to_wsgi_list())

    # Return a Werkzeug Request object
    return WerkzeugRequest(environ)