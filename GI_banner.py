from typing import Union
from datetime import datetime
from GI_datetime import GenshinDatetime, servers_timezone
from GI_servertime import GenshinImpactServerTime


class GenshinBanner:

    def __init__(self, name: str = None, url_fandom: str = None, url_official: str = None, wish_type: str = None,
                 image: str = None, status: str = None,
                 start: Union[datetime, list, str] = None, start_format: str = None,
                 end: Union[datetime, list, str] = None, end_format: str = None, ):

        self.name = name
        self.url_fandom = url_fandom
        self.image = image
        self.url_official = url_official
        self.wish_type = wish_type
        self.status = status

        self.start = []
        if start and not isinstance(start,list):
            for region in servers_timezone.keys():
                self.start.append(GenshinImpactServerTime(region, start, start_format))
        elif start and isinstance(start,list):
            if len(start) != len(servers_timezone.keys()):
                raise ValueError(f'start attribute has {len(start)} times/regions,{len(servers_timezone.keys())}'
                                 f' are needed ({servers_timezone.keys()})')
            else:
                self.start = start

        self.end = []
        if end and not isinstance(end,list):
            for region in servers_timezone.keys():
                self.end.append(GenshinImpactServerTime(region, end, end_format))
        elif end and isinstance(end,list):
            if len(end) != len(servers_timezone.keys()):
                raise ValueError(f'end attribute has {len(end)} times/regions,{len(servers_timezone.keys())}'
                                 f' are needed ({servers_timezone.keys()})')
            else:
                self.end = end

    def __hash__(self):
        return hash((self.name, self.status, self.url_fandom))

    def __eq__(self, other):
        if isinstance(other, GenshinBanner):
            return (self.name, self.status,self.url_fandom) == (other.name, other.status,other.url_fandom)
        return False

    def remain_time(self, server, normalize_delta=False):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            if self.end:
                server_end_time = \
                    [genshin_server_time for genshin_server_time in self.end if genshin_server_time.region == server][0]

                if normalize_delta:
                    return str(server_end_time.server_time - GenshinDatetime.now().to_server(server) +
                               server_end_time.server_time.dst()).split('.')[0]
                else:
                    return server_end_time.server_time - GenshinDatetime.now().to_server(
                        server) + server_end_time.server_time.dst()
            else:
                return None

    def time_until(self,server, normalize_delta=False):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            if self.start:
                server_start_time = \
                    [genshin_server_time for genshin_server_time in self.start if genshin_server_time.region == server][0]

                if normalize_delta:
                    return str(server_start_time.server_time - GenshinDatetime.now().to_server(
                        server)).split('.')[0]
                else:
                    return server_start_time.server_time - GenshinDatetime.now().to_server(
                        server)
            else:
                return None

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

        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        elif not self.end:

            return None
        else:
            time = [genshin_server_time.server_time for genshin_server_time in self.end if
                    genshin_server_time.region == server][0]
            return time + time.dst()

    def set_start_time(self, datetime_str: str, str_format: str):
        for region in servers_timezone.keys():
            self.start.append(GenshinImpactServerTime(region, datetime_str, str_format, True))

    def set_end_time(self, datetime_str: str, str_format: str):
        for region in servers_timezone.keys():
            self.end.append(GenshinImpactServerTime(region, datetime_str, str_format))

    def print_info(self):

        print(f'Name: {self.name}')
        print(f'Fandom URL: {self.url_fandom}')
        print(f'Official URL: {self.url_official}')
        print(f'Status: {self.status}')
        print(f'Type: {self.wish_type}')
        print(f'Image: {self.image}')
        print('Duration:')
        for server in servers_timezone.keys():
            print(f'\t- {server.capitalize().replace("_", " ")} - From: {self.get_start_time(server)} '
                  f'to {self.get_end_time(server)}')
        if self.status == "Current":
            print('Remain Time:')
            for server in servers_timezone.keys():
                print(f'\t- {server.capitalize().replace("_", " ")}: {self.remain_time(server, True)}')
        else:
            print('Time until:')
            for server in servers_timezone.keys():
                print(f'\t- {server.capitalize().replace("_", " ")}: {self.time_until(server, True)}')

    def asdict(self):
        return {
            "name": self.name,
            "url_fandom": self.url_fandom,
            "url_official": self.url_official,
            "status": self.status,
            "wish_type": self.wish_type,
            "image": self.image,

            "start": [start_date.asdict() for start_date in self.start],
            "end": [end_date.asdict() for end_date in self.end]
        }
