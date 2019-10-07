import pandas as pd
import requests as r
import folium


class Outcode:
    """
    Class to hold postcode name, latitude and longitude for a region
    """

    def __init__(
        self, partial_code: str, outcode: str, latitude: float, longitude: float
    ):
        self.partial_code = partial_code
        self.outcode = outcode
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "{}, partial: {} outcode: {}, lat: {}, long: {}".format(
            self.__class__.__name__,
            self.partial_code,
            self.outcode,
            self.latitude,
            self.longitude,
        )

    def __str__(self):
        return repr(self)


class PostcodesIO:
    """Class to hold urls for https://postcodes.io/ API"""

    base_url = "http://api.postcodes.io/"
    postcode_api_url = base_url + "postcodes/"
    autocomplete = postcode_api_url + "{}/autocomplete?limit={}"
    single_postcode_url = postcode_api_url
    bulk_postcode_url = postcode_api_url
    outcode_url = base_url + "outcodes/"


def get_outcode(partial_postcode: str) -> Outcode:
    outcode_information = get_outcode_from_partial(partial_postcode)
    return Outcode(
        partial_postcode,
        outcode_information["outcode"],
        outcode_information["latitude"],
        outcode_information["longitude"],
    )


def get_outcode_from_partial(partial_postcode: str) -> dict:
    """
    Method to get outcode from a partial match. Note this fails silently if not enough information is passed
    :param partial_postcode:
    :return:
    """
    max_limit = 100
    autocomplete_request = r.get(
        PostcodesIO.autocomplete.format(partial_postcode, max_limit)
    )
    autocomplete_request.raise_for_status()
    matching_postcodes = autocomplete_request.json()["result"]
    if len(matching_postcodes) == 0:
        raise ValueError("No data found")
    first_postcode = matching_postcodes[0]
    first_postcode_request = r.get(PostcodesIO.single_postcode_url + first_postcode)
    first_postcode_request.raise_for_status()
    outcode = first_postcode_request.json()["result"]["outcode"]
    outcode_request = r.get(PostcodesIO.outcode_url + outcode)
    outcode_request.raise_for_status()
    return outcode_request.json()["result"]


def get_folium_map(num_postcodes=5):
    postcodes = pd.read_csv("postcodes.csv").iloc[:num_postcodes]
    # Start around UK
    m = folium.Map(location=[55, 4], zoom_start=5)
    for partial_postcode in postcodes["postcode"]:
        outcode = get_outcode(partial_postcode)
        print(outcode)
        folium.Marker(
            location=[outcode.latitude, outcode.longitude],
            popup=outcode.partial_code,
            icon=folium.Icon(color="red"),
        ).add_to(m)
    return m


if __name__ == "__main__":
    get_folium_map()
