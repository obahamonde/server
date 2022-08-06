from random import choice
from uuid import uuid4
from rich.console import Console

BASE = 'https://random-data-api.com/api'
APIS = [
    "/address/random_address", "/appliance/random_appliance",
    "/app/random_app", "/bank/random_bank", "/beer/random_beer",
    "/blood/random_blood", "/business_credit_card/random_card",
    "/cannabis/random_cannabis", "/code/random_code", "/coffee/random_coffee",
    "/commerce/random_commerce", "/company/random_company",
    "/computer/random_computer", "/crypto/random_crypto",
    "/crypto_coin/random_crypto_coin", "/color/random_color",
    "/dessert/random_dessert", "/device/random_device", "/food/random_food",
    "/name/random_name", "/hipster/random_hipster_stuff",
    "/invoice/random_invoice", "/users/random_user", "/stripe/random_stripe",
    "/subscription/random_subscription", "/vehicle/random_vehicle",
    "/id_number/random_id_number", "/internet_stuff/random_internet_stuff",
    "/lorem_ipsum/random_lorem_ipsum", "/lorem_flickr/random_lorem_flickr",
    "/lorem_pixel/random_lorem_pixel", "/nation/random_nation",
    "/number/random_number", "/phone_number/random_phone_number",
    "/placeholdit/random_placeholdit", "/restaurant/random_restaurant"
]

COLORS = [
    'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'black',
]

def random_urls(size: int, qty:int):
    return [f'{BASE}/{choice(APIS)}?size={size}' for i in range(1, qty)]

def get_avatar():
    return f"https://avatars.dicebear.com/api/bottts/{uuid4().hex}.svg"

def log(msg:str, color:str='cyan'):
    Console().log(msg, style=color)

def uid():
    return uuid4().hex
