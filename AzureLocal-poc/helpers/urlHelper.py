from urllib.parse import urlparse

def url_parser(url):
   parsed_url = urlparse(url)
   path = parsed_url.path.lower()
   return path