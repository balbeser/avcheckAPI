import requests

api_key = ""

class Avcheck(object):
    def __init__(self, file_path: str) -> None:
        self.apikey : str = api_key
        self._path : str = file_path
        self.detects : list = []
        self._detects : str = ""
        self._data : list = []
        self.file_name : str = ""
        self.check_id : str = ""

    def get_data(self):
        data = {"apikey": self.apikey, "task_type": "file"}
        with open(self._path, "rb") as doc:
            self._data = requests.post("http://avcheck.net/vhm/api/v1/check/new/", files={'file': doc}, data=data).json()

    def check(self):
        self.get_data()
        self._detects = str(self._data["data"]["info"]["duration"])
        self.file_name = str(self._data["data"]["info"]["object_name"])
        self.check_id = str(self._data["data"]["info"]["check_id"])
        for i in self._data["data"]["results"]:
            detect_name = self._data["data"]["results"][i]["objects"][self._path]["detect_name"]
            if detect_name not in self.detects:
                status = None if detect_name == '' else detect_name
                self.detects.append({"status": status, "service": i, "detect_name": detect_name})


if __name__ == "__main__":
    file = input("Drag file: ")
    avcheck = Avcheck(file)
    detects = avcheck.check
    print("Total: "+detects._detects)
    for i in detects.detects:
        status = "+" if i["status"] else "-"
        detect = i["detect_name"] if i["status"] else "[CLEAN]"
        print(status+" Antivirus: "+i["service"]+" | Detect: "+detect)
