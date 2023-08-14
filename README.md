# Note to self

## Parameters
There are two ways to include a specific value into an HTTP request:
1. **Path parameter**: it a parameter that follow `/` in the URL defining a new API route.
2. **Query parameter**: it may be treated as a filtering condition using the form `?<key>=<value>`, where `<key>` and `<value>` are field and value of interest to filter, respectively (separated by `&` if more than one key-value pairs are involved).

> `%20` refers to a space in URL.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

In this example, `item_id` is a path parameter captured from the URL, while `q` is a query parameter that is optional and can be provided in the URL like this: `/items/42?q=search_term`.

In summary, path parameters are used for essential identifying information in the URL structure, while query parameters are used for optional and supplementary information that can modify the behavior of the endpoint.

## Status codes
A status code contains 3 digits which represents different scenario of a situation when sending an HTTP request from a client to a server. It can be divided into 5 categories:
1. `1xx`: information response.
2. `2xx`: success.
3. `3xx`: redirection (requires some actions to process first).
4. `4xx`: client error.
5. `5xx`: server error.

## Json Web Token (JWT)
* It is an object to securely transmit data between two parties using json object.
* It is usually used in auuthentication process.
* It contains header (cryptographic algorithm used to encode/decode), payload (data), and signature (encoded content).
* Please visit: [jwt.io](https://jwt.io) for more information.

> it requires a secret key which can be found from running `openssl rand -hex 32`.