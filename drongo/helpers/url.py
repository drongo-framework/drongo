class URLHelper(object):
    """Helper class with using urls within the class"""

    @classmethod
    def url(cls, pattern, method='GET'):
        """Decorator to mark url pattern for a callable

        Args:
            pattern (:obj:`str`): URL pattern to add. This is usually '/'
                separated path. Parts of the URL can be parameterised using
                curly braces.
                Examples: "/", "/path/to/resource", "/resoures/{param}"
            method (:obj:`str`, :obj:`list` of :obj:`str`, optional): HTTP
                methods for the path specied. By default, GET method is added.
                Value can be either a single method, by passing a string, or
                multiple methods, by passing a list of strings.

        Note:
            A trailing '/' is always assumed in the pattern.
        """
        def _inner(func):
            setattr(func, '__drongo_url_pattern', pattern)
            setattr(func, '__drongo_url_method', method)
            return func

        return _inner

    @classmethod
    def mount(cls, app, instance, base_url=''):
        """Mount an instance with methods marked with url on to a drongo app.

        Args:
            app: Drongo app instance.
            instance: Instance that contains methods with url decorator.
            base_url: URL prefix for all the url patterns used.
        """
        for attr in dir(instance):
            attr = getattr(instance, attr)
            if hasattr(attr, '__drongo_url_pattern'):
                app.add_url(
                    pattern=base_url + getattr(attr, '__drongo_url_pattern'),
                    method=getattr(attr, '__drongo_url_method'),
                    call=attr
                )

    @classmethod
    def endpoint(cls, app, klass, base_url=''):
        """Registers Endpoint class with the app

        Args:
            app: Drongo app instance
            klass: Class to register
        """
        app.add_url(
            pattern=base_url + klass.__url__,
            method=klass.__http_methods__,
            call=klass.do
        )
