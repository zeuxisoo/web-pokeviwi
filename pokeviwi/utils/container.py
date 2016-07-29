class ApiContainer(object):

    users = {}

    def add(self, username, api):
        self.users[username] = api

    def get(self, username):
        return self.users[username]
