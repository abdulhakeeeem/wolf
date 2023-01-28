class Banned:
    def __init__(self, words, starts, delete, users=None, channels=None, response=None, privMsg=None, privMsgUsers=None, timeout=None, deleteAfter=None):
        self.words = words
        self.starts = tuple(starts) if starts else None
        self.delete = delete
        self.users = users
        self.channels = channels
        self.res = response
        self.privMsg = privMsg
        self.privMsgUsers = privMsgUsers
        self.timeout = timeout
        self.deleteAfter = deleteAfter

    def isBanned(self, message):

        if (self.channels and message.channel.id not in self.channels) or (self.users and message.author.id not in self.users):
            return False

        if self.starts:
            if not message.content.lower().startswith(self.starts):
                return False

        if self.words:
            for word in self.words:
                if word in message.content.lower():
                    return True

        if not self.words:
            return True

        return False

    def _format(self,message, response):
        if not response:
            return None

        return response.replace('{mention}', f'<@{message.author.id}>')

    def response(self, message):
        if not self.res:
            return None

        return self._format(message, self.res)

    def privateResponse(self, message):
        if not self.privMsg:
            return None

        return self._format(message, self.privMsg)



