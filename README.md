# Semantic Mediawiki Export Scripts

In this repo we explore ways of accessing and exporting data stored in a Semantic Mediawiki.

## Accessing page texts

To access page contents, the standard Mediawiki API can be used as [described here](https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page).

Semantic properties are present as the templates created by PageForms, but lacking information such as property names, types etc.


## Accessing rdf properties

Property information for pages cann be accessed via the `/index.php?title=Special:ExportRDF/<Pagename>&syntax=rdf` endpoint. This is not part of the MediaWiki Api. Therefore, if we want to query this site in a private wiki, we have to use the [`clientlogin` action](https://www.mediawiki.org/wiki/API:Login#Method_2._clientlogin) of the API (or the OATH extension).

In order to the `clientlogin` action, the read permissions of the user group who wishes to access the information needs to set to `true` in the `LocalSettings.php`.


## `prototype.py`

In order to work, the prototype needs a config file `config.yml` in the same directory:

```yaml
url: "http://127.0.0.1:8080/" # base url
api: "http://127.0.0.1/api.php" # api url
lgname: <username> # MediaWiki username with read permissions
lgpassword: <password> 
```

## License

MIT