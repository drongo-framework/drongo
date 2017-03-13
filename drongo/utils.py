class dict2(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self.setdefault(name, dict2())
