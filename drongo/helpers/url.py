class URLHelper(object):
    @classmethod
    def url(cls, pattern, method='GET'):
        def _inner(func):
            setattr(func, '__drongo_url_pattern', pattern)
            setattr(func, '__drongo_url_method', method)
            return func

        return _inner

    @classmethod
    def mount(cls, app, instance, base_url=''):
        for attr in dir(instance):
            attr = getattr(instance, attr)
            if hasattr(attr, '__drongo_url_pattern'):
                app.add_url(
                    pattern=base_url + getattr(attr, '__drongo_url_pattern'),
                    method=getattr(attr, '__drongo_url_method'),
                    call=attr
                )
