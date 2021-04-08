import requests
import rdflib
import urllib
import re
from .ns import SMW, WIKI_PAGE


class MediawikiApi:
    """
    Wrapper class for the Mediawiki API.
    """

    template_re = re.compile("{{.*?}}", re.DOTALL)    

    def __init__(self, url, api, lgname, lgpassword, verbose=False):
        """
        Initializes MediawikiApi object.

        :param url: URL of the Mediawiki
        :param api: URL of the Mediawiki API
        :param lgname: Username (Mediawiki user with read/write permissions)
        :param lgpassword: Password
        :param verbose: Display additional information
        :return: Returns nothing
        """
        self._url = url
        self._api = api
        self._lgname = lgname
        self._lgpassword = lgpassword
        self._session = requests.Session()
        self._verbose = verbose

        login_token = self._get_login_token()
        self._login(login_token)


    def _get_login_token(self):
        """
        Fetches login token from the Mediawiki API

        :return: Returns login token
        """
        token_params = {
            'action':"query",
            'meta':"tokens",
            'type':"login",
            'format':"json"
        }
        rsp = self._session.get(url=self._api, params=token_params)
        data = rsp.json()
        return data["query"]["tokens"]["logintoken"]


    def _get_csrf_token(self):
        """
        Fetches CSRF token from the Mediawiki API.

        :return: Returns CSRF token
        """
        token_params = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }
        rsp = self._session.get(url=self._api, params=token_params)
        data = rsp.json()
        return data["query"]["tokens"]["csrftoken"]       


    def _login(self, login_token):
        """
        Login to mediawiki

        :param login_token: Mediawiki API login token
        :return: Returns nothing
        """
        login_params = {
            "action": "clientlogin",
            "loginreturnurl": self._url,
            "logintoken": login_token,
            "username": self._lgname,
            "password": self._lgpassword,
            "format": "json"
        }
        rsp = self._session.post(url=self._api, data=login_params)
        if self._verbose:
            print(f"Logged in as user <{self._lgname}>")


    def fetch_category(self, category):
        """
        Fetches all pages in a category.

        :param category: Category name.
        :return: List of page titles
        """
        fetch_params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:" + category,
            "cmlimit": 200,
            "format": "json"
        }
        rsp = self._session.get(url=self._api, params=fetch_params)
        data = rsp.json()

        category_pages = []
        for entry in data["query"]["categorymembers"]:
            category_pages.append(entry["title"])
        
        return category_pages

    def _get_page_free_text(self, wikitext):
        free_text = self.template_re.sub("", wikitext).strip()
        return free_text


    def _fetch_page_rdf_graph(self, page):
        rdf_url = f"{self._url}index.php?title=Special:ExportRDF/{page}&syntax=rdf"
        rsp = self._session.get(rdf_url)

        g = rdflib.Graph()
        g.parse(data=rsp.text, format="xml")  

        return g


    def _get_property_information(self, prop_uri):
        page_title = str(prop_uri).split("Special:URIResolver/")[-1]
        g = self._fetch_page_rdf_graph(page_title.replace("-3A", ":"))

        label = str(g.label(prop_uri))
        data_type = g.value(
            subject=prop_uri, 
            predicate=SMW.type,
            object=None)

        return {
            "uri": prop_uri,
            "label": label,
            "type": data_type
        }


    def _get_page_label(self, page_uri):
        page_title = str(page_uri).split("Special:URIResolver/")[-1]
        page_title = page_title.replace("_", " ")
        return urllib.parse.unquote(page_title.replace("-", "%"))
        

    def _get_page_semantic_properties(self, page):
        g = self._fetch_page_rdf_graph(page)

        page_uri = g.value(
            subject=None, 
            predicate=rdflib.RDFS.label, 
            object=rdflib.Literal(page))

        properties = []
        for s, p, o in g.triples((page_uri, None, None)):          
            if "Property" in str(p):
                prop_data = self._get_property_information(p)
                if prop_data["type"]:

                    if prop_data["type"] == WIKI_PAGE:
                        value_label = self._get_page_label(o)
                        properties.append({
                            "property": prop_data,
                            "value": o,
                            "label": value_label
                        })
                    else:
                        properties.append({
                            "property": prop_data,
                            "value": str(o)
                        })
        
        return properties
            

    def fetch_page(self, page):
        """
        TODO 
        Fetches a SMW page and its semantic properties.

        ## Accessing page texts
        To access page contents, the standard Mediawiki API can be used as described here: 
        https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page.
        Semantic properties are present as the templates created by PageForms, 
        but lacking information such as property names, types etc.

        ## Accessing rdf properties
        Property information for pages cann be accessed via the 
        `/index.php?title=Special:ExportRDF/<Pagename>&syntax=rdf` endpoint. 
        This is not part of the MediaWiki Api. Therefore, if we want to query this site in 
        a private wiki, we have to use the `clientlogin` action 
        (https://www.mediawiki.org/wiki/API:Login#Method_2._clientlogin) of the API 
        (or the OATH extension). In order to the `clientlogin` action, the read permissions of 
        the user group who wishes to access the information needs to set to `true` 
        in the `LocalSettings.php`.

        """
        
        if self._verbose:
            print(f"fetching page <{page}> ...")

        fetch_params = {
            "action": "parse",
            "page": page,
            "prop": "wikitext",
            "formatversion": 2,
            "format": "json"
        }
        rsp = self._session.get(url=self._api, params=fetch_params)
        data = rsp.json()
        wikitext = data["parse"]["wikitext"]
        free_text = self._get_page_free_text(wikitext)
        properties = self._get_page_semantic_properties(page)
       
        return {
            "title": page,
            "properties": properties,
            "free_text": free_text
        }


    def create_page(self, title, content):
        """
        Creates a wiki page.

        :param title: Page title
        :content: Page content
        :return: Returns nothing
        """
        csrf_token = self._get_csrf_token()
        payload = {
            "action": "edit",
            "title": title,
            "token": csrf_token,
            "format": "json",
            "text": content
        }
        rsp = self._session.post(url=self._api, data=payload)
        if self._verbose:
            print(f"... page '{title}' created")