# Spider
An asynchronous server made in pure python

# Installation

## Requirements
- Python >= 3.9
- A spare brain cell 🧠

## Install
Coming soon...

# Usage

## Example Web Server
```python
from spider import Server, serve
from spider.web import WebService, HTTPResponse

@serve
class MyWebServer(Server):
    service = WebService
    routes = {
        r"^/?$": HTTPResponse("Hello World!")
    }
```

## Example API Endpoint
```python
from spider import Server, serve
from spider.web import WebService, responses

def my_api(request):
    return responses.JSONResponse({
        "path": request.path,
        "params": str(request.params),
        "body": request.body_json
    })

@serve
class MyAPIEndpoint(Server):
    service = WebService
    routes = {
        r"^/foo/bar/?$": my_api
    }
```