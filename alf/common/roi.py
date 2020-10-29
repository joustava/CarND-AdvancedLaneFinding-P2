import numpy


class Roi(object):
    @staticmethod
    def vertices(width, height, k=0.54):
        """
        Creates the vertices to denote a region of interest.
        """
        return numpy.array([
            [
                (0, height),
                (width, height),
                (width//2 - 25, height * k),
                (width//2 + 25, height * k)
            ]], dtype=numpy.int)
