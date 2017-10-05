"""Utility classes for use with Drongo"""


UNSET = object()


class dict2(dict):
    """Extended dict class.

    This class allows access to dict items as members
    """
    def __setattr__(self, name, value):
        if name.startswith('__'):
            return super(dict2, self).__setattr__(name, value)
        if isinstance(value, dict):
            value = self.from_dict(value)

        self[name] = value

    def __getattr__(self, name):
        if name.startswith('__'):
            return super(dict2, self).__getattr__(name)
        return self.setdefault(name, dict2())

    def get_property(self, prop):
        """Access nested value using dot separated keys

        Args:
            prop (:obj:`str`): Property in the form of dot separated keys

        Returns:
            Property value if exists, else `None`
        """
        prop = prop.split('.')
        root = self
        for p in prop:
            if p in root:
                root = root[p]
            else:
                return None
        return root

    def update(self, other):
        for k, v in other.items():
            if k in self and isinstance(v, dict) and isinstance(self[k], dict):
                self[k].update(v)
            else:
                setattr(self, k, v)

    @classmethod
    def from_dict(cls, val):
        """Creates dict2 object from dict object

        Args:
            val (:obj:`dict`): Value to create from

        Returns:
            Equivalent dict2 object.
        """
        if isinstance(val, dict2):
            return val

        elif isinstance(val, dict):
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

    def to_dict(self, val=UNSET):
        """Creates dict object from dict2 object

        Args:
            val (:obj:`dict2`): Value to create from

        Returns:
            Equivalent dict object.
        """
        if val is UNSET:
            val = self

        if isinstance(val, dict2) or isinstance(val, dict):
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
