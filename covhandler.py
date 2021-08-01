from covapi import CowinAPI
from pprint import pprint
import functools

center_level_keys = ['fee_type']


class CowinDataHandler(CowinAPI):
    def __init__(self) -> None:
        super().__init__()

    def argument_validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            excempt_keys = ['exclude_pincode']
            allowed_key_value_pairs = {
                'fee_type': ['Paid', 'Free'],
                'vaccine': ['COVISHIELD', 'COVAXIN'],
                'min_age_limit': [18, 45],
                'allow_all_age': [True, False],
                'dose_number': [1, 2]
            }
            for key, value in kwargs.items():
                if key in excempt_keys:
                    continue
                if value not in allowed_key_value_pairs[key]:
                    raise ValueError('{} is Invaild value for {} argument\n Valid Values can be {}'.format(
                        value, key, ",".join([str(v) for v in allowed_key_value_pairs[key]])))
            return func(*args, **kwargs)
        return wrapper

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

    @staticmethod
    def check_dose_availablity(data, dose_number):
        new_data = list()
        if dose_number == 1:
            key = 'available_capacity_dose1'
        else:
            key = 'available_capacity_dose2'

        for center in data:
            for session in center.get('sessions'):
                if session.get(key) > 0:
                    new_data.append(center)

        return new_data

    @staticmethod
    def exclude_data_with_these_pincodes(data, pincodes):
        new_data = list()
        for center in data:
            if center.get('pincode') not in pincodes:
                new_data.append(center)
        return new_data

    @argument_validator
    def data_parser(self, data, *args, **kwargs):
        for key, value in kwargs.items():
            if key == 'dose_number':
                data = self.check_dose_availablity(data, value)

            elif key == 'exclude_pincode':
                data = self.exclude_data_with_these_pincodes(data, value)

            elif key in center_level_keys:
                data = self.filter_data(data, key, value)

            else:
                data = self.filter_data(data, key, value, in_session=True)

        return data

    def covcaller(self, *args, **kwargs):
        data, status = self.get_avail_disricts(args[0])
        if status == 200:
            _filter_data = self.data_parser(data, *args, **kwargs)
            return _filter_data
        else:
            return data

if __name__ == '__main__':
    obj = CowinDataHandler()
    d = {
        'fee_type': 'Paid',
        'vaccine': 'COVISHIELD',
        'min_age_limit': 18,
        'allow_all_age': True,
        'dose_number': 1,
        'exclude_pincode': [401501]
    }
    obj.covcaller(394, **d)
