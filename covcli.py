from pprint import pprint
from click.termui import prompt
from covhandler import CowinDataHandler
import click

def filter_data(data):
    new_data = list()
    for center in data:
        new_dict = {
            'center_id' : center.get('center_id'),
            'district_name' : center.get('district_name'),
            'address' : center.get('address'),
            'pincode' : center.get('pincode'),
            'name' : center.get('name'),
            'block_name' : center.get('block_name'),
            'fee_type' : center.get('fee_type')
        }
        new_data.append(new_dict)
    return new_data

@click.command()
@click.option('--district', default=394, prompt=True)
@click.option('--fee_type', default="Free", prompt=True)
@click.option('--vaccine', default="COVISHIELD", prompt=True)
@click.option('--min_age_limit', default=18, prompt=True)
@click.option('--allow_all_age', default=True, prompt=True)
@click.option('--dose_number', default=1, prompt=True)
@click.option('--avoid_pincode', default="", required=False)
@click.option('--detail', default=False, required=False)
def cli(district, fee_type, vaccine, min_age_limit, allow_all_age, dose_number, avoid_pincode, detail):
    d = {
        'fee_type': fee_type,
        'vaccine': vaccine,
        'min_age_limit': min_age_limit,
        'allow_all_age': allow_all_age,
        'dose_number': dose_number
    }
    if avoid_pincode:
        pincodes = [int(p.strip()) for p in avoid_pincode.split(',')]
        d.update({'exclude_pincode':pincodes})
    obj = CowinDataHandler()
    data = obj.covcaller(district, **d)
    if detail == False:
        data = filter_data(data)
    click.echo(data)
    
