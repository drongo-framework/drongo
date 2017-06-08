# drongo [![Build Status](https://api.travis-ci.org/drongo-framework/drongo.svg?branch=master)](https://travis-ci.org/drongo-framework/drongo) [![Coverage](https://codecov.io/github/drongo-framework/drongo/coverage.svg?branch=master)](https://codecov.io/github/drongo-framework/drongo/)
A nano web-framework.

## Getting Started
```
from drongo import Drongo

app = Drongo()

@app.url('/')
def index(ctx):
    return 'Hello World!'
```
