import datetime
import requests
import jsunpack

from bs4 import BeautifulSoup


class ACI:
    """
    A class to hold information regarding the plugin.
    """

    # aci = {"shows": [], "movies": [], "cable": []}
    aci = {"shows": {}, "cable": {}, "movies": {}}

    timestamp = None

    _index = str
    _index_soup = None
    _base_url = "https://www.arconaitv.us/"

    def __init__(self):
        """

        """
        index = requests.get(self._base_url).text
        html = index.encode('ascii', 'ignore')
        self._index_soup = BeautifulSoup(html, 'html.parser')

    def load_aci(self):
        """

        :return:
        """
        self.parse_shows()
        self.parse_cable()
        self.parse_movies()

    def update_aci_shows(self):
        """

        :return:
        """
        self._update_shows()

    def update_aci_cable(self):
        """

        :return:
        """
        self._update_cable()

    def update_aci_movies(self):
        """

        :return:
        """
        self._update_movies()

    def parse_shows(self):
        """

        :return:
        """
        # Get shows:
        shows = self._index_soup.find("div", id="shows")
        boxes = shows.find_all("div", class_="box-content")
        for box in boxes:
            if box.a is not None:
                title = str(box.a["title"].strip())
                location = str(box.a["href"])
                location_id = location.split("=")[1]

                # Append the title and the reference to the dictionary
                # shows_list = self.aci["shows"]
                # new_item = {"reference_id": reference_id, "name": title, "thumb": "", "video": "",
                #             "reference": self._base_url + reference}
                # shows_list.append(new_item)

                # Add the new show item.
                shows_dict = self.aci["shows"]
                shows_dict[location_id] = {
                    "title": title,
                    "location": self._base_url + location,
                    "thumbnail": ""
                }

    def parse_cable(self):
        """

        :return:
        """
        # Get cable:
        cable_events = self._index_soup.find("div", id="cable")
        boxes = cable_events.find_all("div", class_="box-content")
        for box in boxes:
            if box.a is not None:
                title = str(box.a["title"].strip())
                location = str(box.a["href"])
                location_id = location.split("=")[1]

                # Append the title and the reference to the dictionary
                # cable_list = self.aci["cable"]
                # new_item = {"name": title, "thumb": "", "video": "", "reference": self._base_url + reference}
                # cable_list.append(new_item)

                # Add the new show item.
                cable_event_dict = self.aci["cable"]
                cable_event_dict[location_id] = {
                    "title": title,
                    "location": self._base_url + location,
                    "thumbnail": ""
                }

    def parse_movies(self):
        """

        :return:
        """
        # Get movies:
        movies = self._index_soup.find("div", id="movies")
        boxes = movies.find_all("div", class_="box-content")
        for box in boxes:
            if box.a is not None:
                title = str(box.a["title"].strip())
                location = str(box.a["href"])
                location_id = location.split("=")[1]

                # Append the title and the reference to the dictionary
                # movies_list = self.aci["movies"]
                # new_item = {"name": title, "thumb": "", "video": "", "reference": self._base_url + reference}
                # movies_list.append(new_item)

                movies_dict = self.aci["movies"]
                movies_dict[location_id] = {
                    "title": title,
                    "location": self._base_url + location,
                    "thumbnail": ""
                }

    def _update_shows(self):
        """

        :return:
        """
        shows_dict = self.aci["shows"]

        for show_id in shows_dict:
            # Get the show item.
            show_item = shows_dict[show_id]

            # print("Visiting: " + str(show_item["location"]))
            page = requests.get(show_item["location"]).text

            html = page.encode('ascii', 'ignore')
            page_soup = BeautifulSoup(html, 'html.parser')
            details = page_soup.find_all("script", {"defer": ""})
            # print(details)
            show_url = self._parse_location(details)
            if show_url is not None:
                show_item["url"] = show_url
                # Get the time in which we last checked the latest link.
                show_item["last_checked"] = self.latest_timestamp()
            else:
                print("Could not retrieve any play details for: " + str(show_item["title"]))

    def _update_cable(self):
        """

        :return:
        """
        cable_dict = self.aci["cable"]

        for cable_event_id in cable_dict:
            # Get cable event item.
            cable_event_item = cable_dict[cable_event_id]

            # print("Visiting: " + str(cable_event_item["location"]))
            page = requests.get(cable_event_item["location"]).text

            html = page.encode('ascii', 'ignore')
            page_soup = BeautifulSoup(html, 'html.parser')
            details = page_soup.find_all("script", {"defer": ""})
            # print(details)
            cable_url = self._parse_location(details)
            if cable_url is not None:
                cable_event_item["url"] = cable_url
                # Get the time in which we last checked the latest link.
                cable_event_item["last_checked"] = self.latest_timestamp()
            else:
                print("Could not retrieve any play details for: " + str(cable_event_item["title"]))

    def _update_movies(self):
        """

        :return:
        """
        movies_dict = self.aci["movies"]

        for movie_id in movies_dict:
            # Get movie item.
            movie_item = movies_dict[movie_id]

            # print("Visiting: " + str(movie_item["location"]))
            page = requests.get(movie_item["location"]).text

            html = page.encode('ascii', 'ignore')
            page_soup = BeautifulSoup(html, 'html.parser')
            details = page_soup.find_all("script", {"defer": ""})
            # print(details)
            movie_url = self._parse_location(details)
            if movie_url is not None:
                movie_item["url"] = movie_url
                # Get the time in which we last checked the latest link.
                movie_item["last_checked"] = self.latest_timestamp()
            else:
                print("Could not retrieve any play details for: " + str(movie_item["title"]))

    @staticmethod
    def latest_timestamp():
        """

        :return:
        """
        dt = datetime.datetime.now()
        timestamp = (dt - datetime.datetime(1970, 1, 1)).total_seconds()
        return timestamp

    @staticmethod
    def _parse_location(details):
        """

        :return:
        """
        play_details = None
        for detail in details:
            if detail is not None and str(detail.string) != "None":
                if "setAttribute" in str(detail.string):
                    play_details = detail.string.strip()

        if play_details is not None:
            # print(play_details)
            # source_details = re.search('source(.*)src', str(play_details))
            # source_group = source_details.group(1)
            # source_list = source_group.split("|")
            # print(source_list)
            #
            # constructed_url = source_list[8] + "://" + source_list[9] + "." + source_list[10] + "/" + \
            #                   source_list[11] + "/" + source_list[7] + "/" + source_list[2] + "/" + \
            #                   source_list[3] + "." + source_list[6]
            # print(constructed_url)

            start_index = play_details.find("eval(function(p,a,c,k,e,")
            end_index = play_details.find("hide")
            packed = play_details[start_index:end_index]
            # print(packed)
            if jsunpack.detect(packed):
                # print(packed)
                unpacked = jsunpack.unpack(packed)
                # print(unpacked)
                unpacked_location = str(unpacked[unpacked.rfind("http"):unpacked.rfind("m3u8") + 4])
                return unpacked_location
            else:
                print("Could not confirm final url.")
                return None
        else:
            return None


if __name__ == "main":
    # Create the ACI class.
    test = ACI()

    # Fetch page info, shows/movies/
    test.load_aci()

    # Get the latest videos for those fetched links.
    test.update_aci_shows()
    test.update_aci_cable()
    test.update_aci_movies()

    # Print final playable items.
    print(test.aci)
