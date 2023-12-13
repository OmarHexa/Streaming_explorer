# FastAPI Documentation

API provides various operations to interact with data using different HTTP methods. The supported operations include:

- POST: Create Data
- GET: Read Data
- PUT: Update Data
- DELETE: Delete Data

Additionally, there are more exotic HTTP methods that may be used in certain scenarios:

- OPTIONS: Retrieve information about the communication options for the target resource. This can include what methods and headers are supported.

- HEAD: Retrieve the headers for a resource without the actual data. This is useful for checking if a resource has changed without downloading the entire content.

- PATCH: Apply partial modifications to a resource. This is typically used for updating only specific fields of an existing resource.

- TRACE: Echoes back the received request, which can be useful for diagnostic purposes.

```python
from fastapi import FastAPI

==app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

return can be `dict`, `list`, singular values as `str`, `int` etc. It can also be `Pydantic models`.

1. Function order matters.
2. Use predefined values e.g. Enum

______________________________________________________________________

### Query parameters

```python
from fastapi import FastAPI
app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

For example, in the URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

______________________________________________________________________

### Request body

A request body is data sent by the client to your API. A response body is the data your API sends to the client.Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time.

```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

Here, we defined a Item model using `Pydantic`and use it as item data type along with path parameter item_id and query parameter q.

We can also use `Annotated` form python `typing` to future declare the limitaton of query parameters along with default value. Please look more into `Annotated` for more details.

```python
from fastapi import Query

q: Annotated[
        str | None, Query(min_length=3, max_length=50, regex="^fixedquery$")
    ] = None,
```

There are several helpful function to add meta-data with path(Path), query(Query),body(BODY), model(Field) parameters.

______________________________________________________________________

@app.get/post/put... function has some additional fields such as response_model and status_code.

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", resonse_model = Dict, status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

______________________________________________________________________

### Error handling

To return HTTP responses with errors to the client you use HTTPException.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        <sup>
        raise HTTPException(status_code=404, detail="Item not found"):</sup>
    return {"item": items[item_id]}
```
