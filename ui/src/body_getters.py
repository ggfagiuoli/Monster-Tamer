class LazyCall:
    def __init__(self, fn, pargs: list = [], kwargs: dict = {}):
        self.fn = fn
        self.pargs = pargs
        self.kwargs = kwargs

    def call(self):
        return self.fn(*self.pargs, **self.kwargs)

    
class BodyGetter:
    def __init__(self, keys: list[str] = [], fns: list[LazyCall] = []):
        self.fns = fns
        self.keys = keys

    def get(self):
        return dict(zip(self.keys, [fn.call() for fn in self.fns]))
