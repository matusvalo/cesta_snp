import random

class RandomUrl(object):
    def __init__(self, urllen, max_tries):
        self.__max_tries = max_tries
        self.__urllen = urllen

    def __iter__(self):
        random.seed()
        for urlnum in range(self.__max_tries):
            yield "".join(random.sample("1234567890abcdefghijklmnopqrstuvwxyz", self.__urllen))
        raise LookupError
