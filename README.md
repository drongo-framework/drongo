# drongo
A nano web-framework.

## Quickstart
```
from drongo import Drongo

app = Drongo()

@app.route('/')
def hello(request):
    return 'Hello World'
```
