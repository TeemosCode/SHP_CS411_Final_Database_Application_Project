from math import sqrt


class Metrics:

    @staticmethod
    def manhattan_dist(x, y):
        assert len(x) == len(y), 'Manhattan dist params must have same length'
        res = 0
        for i in range(len(x)):
            res += abs(x[i] - y[i])
        return res

    @staticmethod
    def euclidean_dist(x, y):
        assert len(x) == len(y), 'Euclean dist params must have same length'
        res = 0
        for i in range(len(x)):
            res += (x[i] - y[i]) ** 2
        return sqrt(res)

    @staticmethod
    def minkowski_dist(x, y, degree=3):
        assert len(x) == len(y), 'Minkowski dist params must have same length'
        res = 0
        for i in range(len(x)):
            res += abs(x[i] - y[i]) ** (degree)
        return res ** (1 / degree)

    @staticmethod
    def cosine_similarity(x, y):
        assert len(x) == len(y), 'Cosine sim params must have same length'
        denox = Metrics.euclidean_dist(x, [0] * len(x))
        denoy = Metrics.euclidean_dist(y, [0] * len(y))
        res = 0
        for i in range(len(x)):
            res += x[i] * y[i]
        return res / denox / denoy if denox!=0 and denoy!=0 else 0

    @staticmethod
    # mimic two pass union algorithm
    def jaccard_similarity(x, y):
        union = set()
        temp = set()
        intersection = set()
        for i in x:
            union.add(i)
            temp.add(i)
        for i in y:
            union.add(i)
            if i in temp:
                temp.remove(i)
                intersection.add(i)
        return 1. * len(intersection) / len(union)

