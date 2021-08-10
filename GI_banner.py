from typing import Union
from datetime import datetime
from GI_datetime import GenshinDatetime, servers_timezone
from GI_servertime import GenshinImpactServerTime


class Banner:

    def __init__(self, name: str = None, url_fandom: str = None, url_official: str = None, status: str = None,
                 start: Union[datetime, GenshinDatetime, str] = None, start_format: str = None,
                 end: Union[datetime, GenshinDatetime, str] = None, end_format: str = None, ):

        self.name = name
        self.url_fandom = url_fandom
        self.url_official = url_official

        self.status = status

        self.start = []
        if start:
            for region in servers_timezone.keys():
                self.start.append(GenshinImpactServerTime(region, start, start_format))
        else:
            self.start = start
        self.end = []
        if end:
            for region in servers_timezone.keys():
                self.end.append(GenshinImpactServerTime(region, end, end_format))
        else:
            self.end = end

    def remain_time(self, server):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            if self.end:
                server_end_time = \
                    [genshin_server_time for genshin_server_time in self.end if genshin_server_time.region == server][0]

                return server_end_time.server_time - GenshinDatetime.now().to_server(
                    server) + server_end_time.server_time.dst()
            else:
                raise ValueError(f'Value {self.end} not valid for end date parameter')

    def get_start_time(self, server):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        elif not self.start:
            return None
        else:
            return [genshin_server_time.server_time for genshin_server_time in self.start if
                    genshin_server_time.region == server][0]

    def get_end_time(self, server):

        print(self.end, server)
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        elif not self.end:

            return None
        else:
            time = [genshin_server_time.server_time for genshin_server_time in self.end if
                    genshin_server_time.region == server][0]
            return (time + time.dst()).strftime("%m/%d/%Y, %H:%M:%S")
