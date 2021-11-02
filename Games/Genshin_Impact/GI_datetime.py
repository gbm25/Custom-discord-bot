import datetime
import pytz

servers_timezone = {
    'asia': pytz.timezone('Asia/Shanghai'),
    'europe': pytz.timezone('Europe/Madrid'),
    'north_america': pytz.timezone('America/New_York')
}


class GenshinDatetime(datetime.datetime):

    def __new__(cls, *args, **kwargs):
        if 'from_datetime' in kwargs.keys():
            my_data = kwargs['from_datetime']

            return super().__new__(cls, my_data.year, my_data.month, my_data.day, my_data.hour, my_data.minute,
                                   my_data.second, my_data.microsecond, my_data.tzinfo)
        else:

            return super().__new__(cls, *args)

    def to_server(self, server: str):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            return self.astimezone(servers_timezone.get(server))

    def set_server(self, server):
        if server not in servers_timezone.keys():
            raise ValueError(f'{server} is not a valid option for parameter "server".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            return servers_timezone.get(server).localize(self)
