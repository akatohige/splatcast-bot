import requests
import json

class StageScheduler():
    def __init__(self):
        self.index = 0
        self.index_max = 12
        self.schedule_dict = None
        self.request_url = "https://spla3.yuu26.com/api/schedule"

    def update(self):
        self.index = 0
        self.schedule_dict = None

        # API: https://spla3.yuu26.com/
        response = requests.get(self.request_url)
        if response.status_code != 200:
            return

        # Parse a text response to json.
        self.schedule_dict = json.loads(response.text)["result"]

    def get_stage(self, index):
        if self.schedule_dict is None:
            return None

        return {
            "regular": self.schedule_dict["regular"][self.index],
            "bankara_challenge": self.schedule_dict["bankara_challenge"][self.index],
            "bankara_open": self.schedule_dict["bankara_open"][self.index],
            "fest": self.schedule_dict["fest"][self.index],
        }
