class ApiContainer(object):

    users = {}

    def add(self, username, api):
        self.users[username] = api

    def get(self, username):
        return self.users[username]

    def remove(self, username):
        if username in self.users:
            return self.users.pop(username)

    def all(self):
        return self.users
