from pgoapi import PGoApi

class PokemonUtils(object):

    api = None

    @classmethod
    def getApi(cls):
        if cls.api is None:
            cls.api = PGoApi()

        return cls.api

