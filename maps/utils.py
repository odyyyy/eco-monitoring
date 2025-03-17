import json

data = json.loads(open('ao.geojson', encoding='utf-8').read())


def get_coordinates_by_name(json_data):
    for feature in json_data['features']:

        coordinates = feature['geometry']['coordinates'][0]
        swapped_coordinates = [[list(reversed(coord)) for coord in polygon] for polygon in coordinates]
        print(swapped_coordinates)

    return None

get_coordinates_by_name(data)

