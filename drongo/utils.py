"""Utility classes for use with Drongo"""


class dict2(dict):
    """Extended dict class.

    This class allows access to dict items as members
    """
    def __setattr__(self, name, value):
        if name.startswith('__'):
            return super(dict2, self).__setattr__(name, value)
        self[name] = value

    def __getattr__(self, name):
        if name.startswith('__'):
            return super(dict2, self).__getattr__(name)
        return self.setdefault(name, dict2())

    @classmethod
    def from_dict(cls, val):
        """Creates dict2 object from dict object

        Args:
            val (:obj:`dict`): Value to create from

        Returns:
            Equivalent dict2 object.
        """
        if isinstance(val, dict):
            res = cls()
            for k, v in val.items():
                res[k] = cls.from_dict(v)
            return res
        elif isinstance(val, list):
            res = []
            for item in val:
                res.append(cls.from_dict(item))
            return res
        else:
            return val

    def to_dict(self, val=None):
        """Creates dict object from dict2 object

        Args:
            val (:obj:`dict2`): Value to create from

        Returns:
            Equivalent dict object.
        """
        val = val or self
        if isinstance(val, dict2):
            res = dict()
            for k, v in val.items():
                res[k] = self.to_dict(v)
            return res
        elif isinstance(val, list):
            res = []
            for item in val:
                res.append(self.to_dict(item))
            return res
        else:
            return val

    def __repr__(self):
        return 'dict2(%s)' % super(dict2, self).__repr__()
