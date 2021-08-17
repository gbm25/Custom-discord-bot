from error_management import create_log


class GenshinCode:

    def __init__(self, promotional_code=None, external_link=None, server=None, rewards=None, status=None, start=None,
                 end=None):
        self.promotional_code = promotional_code
        self.external_link = external_link
        self.server = server
        if not rewards:
            self.rewards = []
        else:
            self.rewards = rewards
        self.status = status
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.promotional_code, self.status, self.start, self.end))

    def __eq__(self, other):
        if isinstance(other, GenshinCode):
            return (self.promotional_code, self.status, self.start, self.end) == (other.promotional_code, other.status, other.start, other.end)
        return False

    def asdict(self):
        return {
            "promotional_code": self.promotional_code,
            "external_link": self.external_link,
            "server": self.server,
            "rewards": [reward.asdict() for reward in self.rewards],
            "status": self.status,
            "start": self.start,
            "end": self.end
        }
