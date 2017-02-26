# drongo
A pico web-framework.

## Quickstart
```
from drongo import Application

app = Application()

@app.route('/')
def hello(request):
    return 'Hello World'
```
