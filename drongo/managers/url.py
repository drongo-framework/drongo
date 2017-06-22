class UrlManager(object):
    def __init__(self):
        self._routes = {}

    def add_url(self, pattern, method=None, call=None):
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
