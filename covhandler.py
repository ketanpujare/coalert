import functools
from covapi import CowinAPI
from pprint import pprint
import pdb

center_level_keys = ['fee_type']


class CowinDataHandler(CowinAPI):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def filter_data(data, key, value, in_session=False):
        new_data = list()
        if in_session == False:
            for center in data:
                if center.get(key) == value:
                    new_data.append(center)
        else:
            for center in data:
                for session in center.get('sessions'):
                    if session.get(key) == value:
                        new_data.append(center)
        return new_data

    def argument_validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            allowed_key_value_pairs = {
                'fee_type': ['Paid', 'Free'],
                'vaccine': ['COVISHIELD', 'COVAXIN']
            }
            for key, value in kwargs.items():
                if value not in allowed_key_value_pairs[key]:
                    raise ValueError('{} is Invaild value for {} argument\n Valid Values can be {}'.format(
                        value, key, ",".join(allowed_key_value_pairs[key])))
            return func(*args, **kwargs)
        return wrapper

    @argument_validator
    def data_parser(self, data, *args, **kwargs):
        for key, value in kwargs.items():
            if key in center_level_keys:
                data = self.filter_data(data, key, value)
            else:
                data = self.filter_data(data, key, value, in_session=True)

        pprint(data)

    def covcaller(self, *args, **kwargs):
        data = self.get_avail_disricts(args[0])
        self.data_parser(data, *args, **kwargs)


obj = CowinDataHandler()
d = {
    'fee_type': 'Paid',
    'vaccine': 'COVAXIN',
    'dose_number': 1
}
obj.covcaller(395, **d)
