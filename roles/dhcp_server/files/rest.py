from __future__ import print_function
import requests
from requests.packages import urllib3

__version__ = '0.1'

UPDATE_URL = "http://127.0.0.1:5000/api/1.0/register/"
DEFAULT_UA = 'Wildsong/%s' % __version__ # This gets logged in REST server
JSON       = 'application/json'

def send(payload):
    """ Send POST request. """
    resp = requests.post(UPDATE_URL, payload)
    #print("Headers from POST request response: ", resp.headers)
    return resp

def get_requests_session():
    requests_session = requests.Session()
    for cls in plugin_manager.get_transport_plugins():
        transport_plugin = cls()
        requests_session.mount(prefix=transport_plugin.prefix,
                               adapter=transport_plugin.get_adapter())
    return requests_session

def get_response(args, config_dir):
    """Send the request and return a `request.Response`."""

    requests_session = get_requests_session()

    if not args.session and not args.session_read_only:
        kwargs = get_requests_kwargs(args)
        if args.debug:
            dump_request(kwargs)
        response = requests_session.request(**kwargs)
    else:
        response = sessions.get_response(
            requests_session=requests_session,
            args=args,
            config_dir=config_dir,
            session_name=args.session or args.session_read_only,
            read_only=bool(args.session_read_only),
        )

    return response

def get_default_headers():
    default_headers = {
        'User-Agent': DEFAULT_UA
    }
    default_headers['Accept'] = 'application/json'
    default_headers['Content-Type'] = JSON
    return default_headers

def get_requests_kwargs(args, base_headers=None):
    """ Translate our `args` into `requests.request` keyword arguments. """

    headers = get_default_headers()
    if base_headers:
        headers.update(base_headers)
    headers.update(args.headers)
    headers = encode_headers(headers)

    credentials = None

    kwargs = {
        'stream': True,
        'method': args.method.lower(),
        'url': args.url,
        'headers': headers,
        'data': data,
        'verify': {
            'yes': True,
            'no': False
        }.get(args.verify, args.verify),
        'cert': cert,
        'timeout': args.timeout,
        'auth': credentials,
        'proxies': dict((p.key, p.value) for p in args.proxy),
        'files': args.files,
        'allow_redirects': args.follow,
        'params': args.params,
    }

    return kwargs

if __name__ == "__main__":

    print("Do a request here.")


        

