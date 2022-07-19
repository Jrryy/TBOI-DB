# The binding of Isaac: Items and scraper

In this project you'll find a json with a list of every item in the game and their metadata, and the scraper I used to generate it.

Feel free to download and modify both the json and the scraper and use them for your own purposes.

## The data

The json contains a list of the following data:
```json
{
    "id": (int) Ingame id of the item,
    "name": (string) The name of the item,
    "quality": (int) Ingame quality of the item,
    "type": (string) Active or passive,
    "recharge": (string | null) How many charges the item needs and how to recharge it,
    "pools": (list[string]) The pools in which the item appears,
    "transformations": (list[string]) The possible transformations the item is part of,
    "expansion": (string) Expansion in which the item was added,
    "style": (list[string]{2}) Values of backgroundPosition, width to show the image of the item
}
```

An example entry for an item would look like this:
```json
{
    "id": 120,
    "name": "Odd Mushroom (Thin)",
    "quality": 2,
    "type": "Passive",
    "recharge": null,
    "pools": [
        "Item Room",
        "Secret Room"
    ],
    "transformations": [
        "Fun Guy"
    ],
    "expansion": "Rebirth",
    "style": [
        "-6452px 0",
        "33px"
    ]
}
```

The `style` key exists because all the items' images are in a sort of sprite map, like this:
![Loooooooooooooooooooooooooooooooooooooooooooooooooooong sprite map](https://platinumgod.co.uk/images/repentance-rebirth-items.png)
And so, we need the offset and width of each item so that it can be properly shown. Using the data in the example, this code below:
```html
<div style="
    width: 33px;
    height: 50px;
    background-image: url('https://platinumgod.co.uk/images/repentance-rebirth-items.png');
    background-position: -6452px 0;
"></div>
```
Would result into this:
<div style="
    width: 33px; 
    height: 50px; 
    background-image: url('https://platinumgod.co.uk/images/repentance-rebirth-items.png'); 
    background-position: -6452px 0;
"></div>

## The scraper

I made the scraper using python 3.8 with the latest versions of requests, beautifulsoup, and cssutils.
Given how simple it is, I've got no reason to believe the script wouldn't work with other versions, either older or newer, of python 3 or the aforementioned modules.