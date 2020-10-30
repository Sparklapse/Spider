class Route():
    def __init__(self, path, domain=r".*", renderer=None):
        self.path = path
        self.domain = domain
        self.renderer = renderer
    
    def __call__(self, *args, **kwargs):
        if not self.renderer:
            if not callable(args[0]):
                raise TypeError(
                    ("Must be a render function that returns a HTTPResponse.\n"
                    f"Returned {args[0]}")
                )
            self.renderer = args[0]
            return self
        else:
            return self.renderer(*args, **kwargs)
