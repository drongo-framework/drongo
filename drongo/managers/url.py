class UrlManager(object):
    """Manages mapping between URL pattern, HTTP methods and callables.

    UrlManager manages mapping betweeen (URL pattern, HTTP methods) and
    callables. It can then retrieve the callable along with parameters from the
    given url path.
    """

    def __init__(self):
        self._routes = {}

    def add_url(self, pattern, method=None, call=None):
        """Add a url pattern

        Args:
            pattern (str): URL pattern to add. This is usually '/' separated
                path. Parts of the URL can be parameterised using curly braces.
                Examples: "/", "/path/to/resource", "/resoures/{param}"
            method (:obj:`str`, :obj:`list` of :obj:`str`, optional): HTTP
                methods for the path specied. By default, GET method is added.
                Value can be either a single method, by passing a string, or
                multiple methods, by passing a list of strings.
            call (callable): Callable corresponding to the url pattern and the
                HTTP method specified.

        Note:
            A trailing '/' is always assumed in the pattern.
        """
        if not pattern.endswith('/'):
            pattern += '/'
        parts = tuple(pattern.split('/')[1:])
        node = self._routes
        for part in parts:
            node = node.setdefault(part, {})
        if method is None:
            node['GET'] = call
        elif isinstance(method, str):
            node[method.upper()] = call
        else:
            for m in method:
                node[m.upper()] = call

    def find_call(self, path, method):
        """Find callable for the specified URL path and HTTP method

        Args:
            path: URL path to match
            method: HTTP method

        Note:
            A trailing '/' is always assumed in the path.
        """
        if not path.endswith('/'):
            path += '/'
        path = path.split('/')[1:]
        return self._recursive_route_match(self._routes, path, method, [])

    def _recursive_route_match(self, node, remaining, method, args):
        # Route is stored in tree form for quick matching compared to
        # traditional form of regular expression matching
        if len(remaining) == 0:
            if callable(node.get(method)):
                return (node.get(method), args)
            else:
                return None

        result = None
        for key in node:
            if key == remaining[0]:
                result = self._recursive_route_match(node[key], remaining[1:],
                                                     method, args)
                if result:
                    return result
            elif len(key) and key[0] == '{':
                # We match for concrete part first and then compare
                # parameterised parts.
                continue

        for key in node:
            if len(key) and key[0] == '{':
                result = self._recursive_route_match(
                    node[key], remaining[1:], method,
                    args + [(key[1:-1], remaining[0])]
                )
                if result:
                    return result
        return None
