from typing import Union

from datetime import datetime

from GI_datetime import GenshinDatetime, servers_timezone


class GenshinImpactServerTime:
    def __init__(self, region: str, dt: Union[datetime, str], datetime_format: str = None):
        if region not in servers_timezone.keys():
            raise ValueError(f'{region} is not a valid option for parameter "region".'
                             f'The value must be one of {servers_timezone.keys()}')
        else:
            self.region = region
        if isinstance(dt, str):
            if datetime_format:
                try:
                    genshin_datetime = GenshinDatetime.strptime(dt, datetime_format)

                    if genshin_datetime.tzinfo:
                        genshin_datetime = genshin_datetime.replace(tzinfo=None)

                    self.server_time = genshin_datetime.set_server(region)

                except ValueError:
                    raise
            else:
                raise ValueError(f'Value {datetime_format}) not valid for parameter "datetime_format". '
                                 f'A valid date time string format is necessary '
                                 f'for the given string date time {dt}')
        else:

            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)

            self.server_time = GenshinDatetime(from_datetime=dt).set_server(region)
