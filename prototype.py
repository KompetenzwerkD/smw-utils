import requests
import yaml
import sys


class MediawikiAPI:

    def __init__(self, url, api, lgname, lgpassword):
        self._url = url
        self._api = api
        self._lgname = lgname
        self._lgpassword = lgpassword
        self._session = requests.Session()

        login_token = self._get_login_token()
        self._login(login_token)


    def _get_login_token(self):
        token_params = {
            'action':"query",
            'meta':"tokens",
            'type':"login",
            'format':"json"
        }
        rsp = self._session.get(url=self._api, params=token_params)
        data = rsp.json()
        return data["query"]["tokens"]["logintoken"]


    def _login(self, login_token):

        login_params = {
            "action": "clientlogin",
            "loginreturnurl": self._url,
            "logintoken": login_token,
            "username": self._lgname,
            "password": self._lgpassword,
            "format": "json"
        }
        rsp = self._session.post(url=self._api, data=login_params)
        data = rsp.json()
        print(data)


    def fetch_category(self, category):
        fetch_params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:" + category,
            "cmlimit": 200,
            "format": "json"
        }
        rsp = self._session.get(url=self._api, params=fetch_params)
        print(rsp.json())


    def fetch_page(self, page):
        # fetch page text
        fetch_params = {
            "action": "parse",
            "page": page,
            "prop": "wikitext",
            "formatversion": 2,
            "format": "json"
        }
        rsp = self._session.get(url=self._api, params=fetch_params)
        print(rsp.json())

        # fetch rdf data
        rdf_url = f"{self._url}index.php?title=Special:ExportRDF/{page}&syntax=rdf"

        rsp = self._session.get(rdf_url)
        print(rsp.text)


if __name__ == "__main__":

    with open("config.yml") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    api = MediawikiAPI(
        config["url"],
        config["api"],
        config["lgname"],
        config["lgpassword"]
    )
    #api.fetch_category("Persons")
    api.fetch_page("Peter Mühleder")