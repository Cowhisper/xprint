



class Theme(object):
    def __init__(self, schemes=None):
        self.schemes = color_schemes
        if schemes is not None:
            self.schemes.update(schemes)
