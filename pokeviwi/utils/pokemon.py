from pgoapi import PGoApi

class PokemonUtils(object):

    api = None

    @classmethod
    def initApi(cls):
        cls.api = PGoApi()

        return cls.api

    @classmethod
    def getApi(cls):
        return cls.api

