__all__ = [
    'NotFoundException',
    'SkipExecException'
]


class NotFoundException(Exception):
    pass


class SkipExecException(Exception):
    pass
