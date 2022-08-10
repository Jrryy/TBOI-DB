import json
import re

import cssutils
import requests
from bs4 import BeautifulSoup

response = requests.get('https://platinumgod.co.uk/repentance')
response.raise_for_status()
css = cssutils.parseUrl('https://platinumgod.co.uk/assets/main.css?v=202111231422')

valid_selector_re = re.compile(r'.*(?:re-itm|rep|abn-itm|apn-itm|bpn-itm)(\d{3}).*')
# The id of the Damocles in the css is wrong. Map it to the right one
css_id_aliases = {
    656: 577,
}

# Map each item with its css rules to be able to show its image
rules = {}
for rule in css.cssRules:
    try:
        matching_item = valid_selector_re.match(rule.selectorText)
    except AttributeError:
        continue
    if matching_item:
        item_id = int(matching_item.group(1))
        item_id = css_id_aliases.get(item_id, item_id)
        rules[item_id] = rule.style.backgroundPosition, rule.style.width if rule.style.width else '50px'

soup = BeautifulSoup(response.content, 'html.parser')
main_div = soup.find('div', 'main')
item_divs = main_div.find_all(recursive=False)

expansion_index = (
    ('Repentance', 2, 'repentance-items2.png'),
    ('Afterbirth +', 6, 'repentance-ap-items.png'),
    ('Afterbirth', 5, 'repentance-ab-items.png'),
    ('Rebirth', 4, 'repentance-rebirth-items.png'),
)

items_list = []
transformation_pattern = re.compile(r'Counts as 1 of 3 .* items needed towards the (.+) transformation\.?')

for expansion, index, image in expansion_index:
    expansion_items_divs = item_divs[index].find_all('li', recursive=False)
    for item_data in expansion_items_divs:
        item_id = item_data.find('p', 'r-itemid')
        item_name = item_data.find('p', 'item-title')
        item_quality = item_data.find('p', 'quality')
        if not all((item_id, item_name, item_quality)):
            raise Exception(f'An item does not have all the expected info.\n{item_data}')

        item_id = int(item_id.string[8:])
        item_name = item_name.string
        item_quality = int(item_quality.string[9:])

        item_image_style = rules[item_id]

        item_transformations = []
        for description in item_data.stripped_strings:
            matching_transformation = transformation_pattern.match(description)
            if matching_transformation:
                item_transformations.append(matching_transformation.group(1))

        other_data_ul = item_data.find('ul')
        if not other_data_ul:
            raise Exception(f'An item does not have the extra data it should have.\n{item_data}')
        other_data_list = other_data_ul.find_all(recursive=False)
        item_type, item_recharge, item_pools = None, None, []
        for other_data in other_data_list:
            text = next(other_data.stripped_strings)
            if text.startswith('Type'):
                item_type = text[6:]
            if text.startswith('Recharge'):
                item_recharge = text[15:].rstrip(' (see above)')
            if text.startswith('Item Pool'):
                item_pools = text[11:].split(', ')
                if item_pools == ['None (see above)']:
                    item_pools = []

        items_list.append({
            'id': item_id,
            'name': item_name,
            'quality': item_quality,
            'type': item_type,
            'recharge': item_recharge,
            'pools': item_pools,
            'transformations': item_transformations,
            'expansion': expansion,
            'style': item_image_style,
            # The clear rune is in a different sprite map
            'image': image if item_id != 263 else 'repentance-rebirth-items.png',
        })

with open('items.json', 'w') as file:
    json.dump(sorted(items_list, key=lambda x: x['id']), file, indent=4)
