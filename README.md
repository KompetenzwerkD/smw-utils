# Semantic Mediawiki Utils

A python module for working  with Semantic Mediawiki 

## Installation

Download repository and use `pip install`

```zsh
$ git clone https://github.com/kompetenzwerkd/smw-utils
$ cd smw-utils
$ pip install .
```

## Usage

### Api Wrapper

Create page 
```python
from smw_utils.api import MediawikiApi

api = MediawikiApi(
   "http://37.120.165.192:8099/",
   "http://37.120.165.192:8099/api.php",
    "username",
    "password
)

api.create_page("Test page", "This page was created via the Mediawiki API")
```

## Author

kompetenzwerkd@saw-leipzig.de

## Copyright

2021, Sächsische Akademie der Wissenschaften zu Leipzig

## License

MIT