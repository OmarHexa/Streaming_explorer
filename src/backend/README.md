## HTTP Request Methods

### GET

- **Description:** The GET method requests data from a specified resource. It retrieves information without altering the state of the server or the resource.

- **Use Case:** Use GET to retrieve data such as web pages, images, or other resources.

```http
GET /api/users
```

### POST

- **Description:** The POST method submits data to be processed to a specified resource. It can result in the creation of a new resource on the server.

- **Use Case:** Use POST to submit form data or upload a file.

```http
POST /api/users
```

### PUT

- **Description:** The PUT method updates a resource or creates a new resource if it doesn't exist at the specified URI.

- **Use Case:** Use PUT to update an existing resource or create a new one if needed.

```http
PUT /api/users/123
```

### PATCH

- **Description:** The PATCH method applies partial modifications to a resource. It is used to apply changes to a part of a resource.

- **Use Case:** Use PATCH when you want to apply partial updates to a resource.

```http
PATCH /api/users/123
```

### DELETE

- **Description:** The DELETE method deletes the specified resource at the given URI.

- **Use Case:** Use DELETE to remove a resource from the server.

```http
DELETE /api/users/123
```

### OPTIONS

- **Description:** The OPTIONS method describes the communication options for the target resource.

- **Use Case:** Use OPTIONS to determine which methods or headers can be used on the resource.

```http
OPTIONS /api/users
```

### HEAD

- **Description:** The HEAD method asks for a response identical to that of a GET request but without the response body.

- **Use Case:** Use HEAD when you only need the headers, not the actual data.

```http
HEAD /api/users/123
```

These are the fundamental HTTP request methods, each serving a specific purpose in interacting with resources on a server. Choose the appropriate method based on the desired action and the semantics of your API.

## REST API: Simplifying Communication in Software Development

API, an acronym for `Application Programming Interface`, is a crucial piece of code that defines how various software components interact programmatically. Behind the scenes of modern user interfaces, numerous requests are sent to API servers to retrieve data, enabling the client to process the information and generate outcomes in the user interface.

### How REST APIs Facilitate Communication

Among various API types, we focus on REST APIs for their widespread use and importance. REST, short for Representational State Transfer, is an architectural style that defines constraints for APIs to adhere to, making them "RESTful."

`REST APIs, a prevalent type, utilize the HTTP protocol for data transmission, categorizing them as web services managing the interaction between client applications and API servers.` Using HTTP, clients send requests to API servers, and the servers respond with encoded data, promoting interoperability across different programming languages.

### Key Characteristics of REST APIs

1. **Statelessness:** REST APIs embrace statelessness, making them ideal for cloud applications, cloud computing, and microservices. This characteristic simplifies communication and enhances scalability.

2. **Interoperability:** The HTTP protocol employed by REST APIs facilitates communication between systems written in different programming languages. This interoperability is a hallmark of modern software development.

### Use Cases of REST APIs

REST APIs find applications across diverse projects, offering separation of concerns between client and server. Common use cases include:

- **Cloud Applications:** REST's statelessness aligns well with cloud applications, ensuring efficient and scalable communication.

- **Cloud Computing:** REST supports cloud computing by controlling how URLs are decoded during client-server communication.

- **Microservices:** REST APIs serve as connectors, linking microservices into a cohesive application.

In summary, REST APIs, guided by the principles of RESTful architecture, play a pivotal role in modern software development, enabling seamless communication and collaboration between diverse systems and platforms.

## Understanding REST API: Anatomy and Core Principles

### Anatomy of REST API Request

REST APIs dictate how client applications and API servers interact, setting rules for sending requests and receiving information. Key components of REST API requests include:

#### 1. Resources

- **Definition:** Resources represent different types of data objects returned by the API.

#### 2. Endpoints

- **Definition:** Endpoints, highlighted in API documentation, are core to requests. Each endpoint corresponds to a different action and has a unique path (e.g., /shows) after the API's base URL.

#### 3. Methods

- **Definition:** HTTP methods indicate actions toward a resource. Common methods include POST (create), GET (read), PUT (update/create), and DELETE (delete).

#### 4. Parameters

- **Definition:** Parameters, like header, path, and query string parameters, influence the response. For example, /pet/{petId} uses a path parameter.

#### 5. Request Body

- **Definition:** JSON objects passed in the body of requests, particularly with POST or PUT methods, serve as request bodies.

### Core Principles of REST

#### 1. Client and Server

- **Principle:** REST separates the client and server, allowing independent evolution. The client doesn't concern itself with server data storage, promoting portability and scalability.

#### 2. Statelessness

- **Principle:** REST maintains statelessness, storing session data only in the client application. Each request is independent, enhancing scalability.

#### 3. Cacheable

- **Principle:** REST APIs indicate whether responses can be cached and specify the duration. Caching optimizes availability and performance by reducing API requests.

#### 4. Uniform Interface

- **Principle:** RESTful APIs must identify resources, use HTTP methods for operations, provide self-descriptive messages, and require clients to use hyperlinks for interactions.

#### 5. Layered System

- **Principle:** REST supports a layered system architecture where each layer has a designated role. This enables a modular approach, including intermediary servers for security and load balancing.

In summary, the anatomy of REST API requests involves resources, endpoints, methods, parameters, and request bodies. The core principles, including client-server separation, statelessness, cacheability, a uniform interface, and a layered system, make REST APIs a robust choice in software development.

## FastAPI for Restful API development

FastAPI is a modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints. It simplifies the development of RESTful APIs, especially for CRUD (Create, Read, Update, Delete) operations. Below is an overview of how FastAPI facilitates the implementation of a RESTful API with CRUD operations:

### 1. **Installation and Setup:**

Firstly, install FastAPI using:

```bash
pip install fastapi
```

Additionally, you'll need an ASGI server; `uvicorn` is a popular choice:

```bash
pip install uvicorn
```

### 2. **Defining a FastAPI App:**

Create a Python file (e.g., `main.py`) and import FastAPI:

```python
from fastapi import FastAPI
```

Create an instance of the FastAPI class:

```python
app = FastAPI()
```

### 3. **Modeling Data:**

Define data models using Pydantic for request and response validation:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
```

### 4. **Creating Endpoints:**

Define endpoints for CRUD operations. For example:

```python
@app.post("/items/")
async def create_item(item: Item):
    # Logic to create item
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Logic to read item with given ID
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # Logic to update item with given ID
    return {"item_id": item_id, "updated_item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # Logic to delete item with given ID
    return {"item_id": item_id, "status": "deleted"}
```

Here's how FastAPI implements a REST API:

### 1. **Declaration of API Routes:**

FastAPI utilizes Python's type hints to declare API routes. Developers can define routes by creating functions that receive parameters with annotated types. These annotations are then used to automatically generate API documentation.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}
```

In the example above, `item_id` is a path parameter, and `query_param` is a query parameter. FastAPI automatically validates the request parameters based on their types.

### 2. **Automatic Validation and Documentation:**

FastAPI uses type hints not only for validation but also for automatic generation of OpenAPI and JSON Schema documentation. This ensures that the API documentation stays in sync with the actual code.

### 3. **Dependency Injection System:**

FastAPI includes a powerful dependency injection system. Dependencies such as authentication, database connections, or custom logic can be injected into route functions, making the code modular and testable.

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_query_param(query_param: str = None):
    return query_param

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = Depends(get_query_param)):
    return {"item_id": item_id, "query_param": query_param}
```

Here, `get_query_param` is a dependency that can be reused across multiple routes.

### 4. **Asynchronous Support:**

FastAPI fully supports asynchronous programming using Python's `async` and `await` syntax. Asynchronous routes enable handling a large number of concurrent connections efficiently.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/async_item/{item_id}")
async def read_item(item_id: int):
    # Perform asynchronous operations
    return {"item_id": item_id}
```

### 5. **Fast (High-Performance):**

FastAPI is built to be fast. It achieves high performance by leveraging Starlette and Pydantic, optimizing request and response handling.

### 6. **Security Features:**

FastAPI includes built-in security features, including OAuth2 authentication and API token handling, making it easy to secure APIs.

In summary, FastAPI simplifies the process of building RESTful APIs in Python by leveraging type hints, automatic validation, dependency injection, asynchronous support, and built-in security features. Its performance and ease of use make it an excellent choice for developers building robust and scalable APIs.

# FastAPI documentation summary

FastAPI simplifies the handling of various parameters in your API routes, providing a clean and Pythonic way to manage path, query, and request body parameters.

### Type Hinting and Data Conversion using Pydantic

FastAPI leverages type hinting in Python to automatically convert and validate path parameters. By using Pydantic models, you can define the expected type and structure of the parameter.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

Here, `item_id` is automatically converted to an integer.

### Python Enum Class for Predefined Values

For predefined values, you can use Python's `Enum` class. It ensures that only specific values are accepted as path parameters.

Example:

```python
from fastapi import FastAPI
from enum import Enum

class ItemEnum(str, Enum):
    foo = "foo"
    bar = "bar"

app = FastAPI()

@app.get("/items/{item_type}")
async def read_item(item_type: ItemEnum):
    return {"item_type": item_type}
```

In this example, only values "foo" or "bar" are valid for the `item_type` path parameter.

FastAPI allows you to define default values for query parameters, making them optional. Additionally, you can mark parameters as required.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

```http
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Here, `skip` and `limit` are optional query parameters with default values, making them optional in the URL.

### Enhancing API Validation and Metadata with FastAPI

FastAPI empowers developers with extensive tools for parameter validation and metadata declaration, offering flexibility and clarity in API development. Here's a detailed explanation of additional validation and metadata incorporation using Query, Path, and Body:

```python
from typing import Annotated

from fastapi import Body, Path, Query, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, regex="^fixedquery$")
    ] = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
```

**Explanation:**

1. **Query, Path, and Body:**
   FastAPI allows the declaration of additional validation and metadata using `Query`, `Path`, and `Body` parameters. These decorators provide a way to specify constraints such as minimum and maximum values, regex patterns, and more.

2. **Default Values and Parameter Requirement:**
   Singular values in the function parameters are interpreted as query parameters by default. Explicitly using `Query` is not necessary. If a parameter lacks a default value (`None` or `Ellipsis(...)`), it becomes a required query parameter.

3. **Validation within Pydantic Models:**
   Validation and metadata can be seamlessly incorporated within Pydantic models using Pydantic's `Field`. While `Query`, `Path`, and `Body` are imported from FastAPI, `Field` is directly imported from Pydantic. This provides a consistent approach for adding constraints both at the operation function level and within Pydantic models.

4. **Annotations for Detailed Metadata:**
   Annotations, such as `Annotated`, allow for attaching detailed metadata to parameters. This includes specifying titles, descriptions, and additional validation criteria. It enhances the documentation and clarity of the API.

By combining FastAPI's parameter decorators and Pydantic's modeling capabilities, developers can ensure robust validation, detailed metadata, and a clean, expressive API design.

______________________________________________________________________

In FastAPI, `@app.get`/`@app.post`/`@app.put`, etc., functions come with additional fields such as `response_model` and `status_code`, enhancing the control and documentation of your API responses. Here's an example:

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

**Explanation:**

1. **Response Model (`response_model`):**

   - Specifies the data model that the endpoint will return in the response.
   - In this example, `response_model=dict` indicates that the endpoint will return a dictionary.
   - This ensures consistency in the structure of the response data.

2. **Status Code (`status_code`):**

   - Defines the HTTP status code that will be included in the response.
   - Here, `status_code=status.HTTP_201_CREATED` signifies that the operation was successful, and the resource was created.

### Error handling

Additionally, FastAPI provides robust error handling capabilities using the `HTTPException` class. Here's an example:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

HTTPException is a normal Python exception with additional data relevant for APIs. Because it's a Python exception, you don't return it, you raise it.

### Requesting Files from client

```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

______________________________________________________________________

<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>

______________________________________________________________________

For additional details and examples, refer to the [FastAPI Request Forms and Files Tutorial](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/).

## Dependency Injection

"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

- Have shared logic (the same code logic again and again).
- Share database connections.
- Enforce security, authentication, role requirements, etc.

All these, while minimizing code repetition. Whenever a new request arrives, FastAPI will take care of:

- Calling your dependency ("dependable") function with the correct parameters.
- Get the result from your function.
- Assign that result to the parameter in your path operation function.

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
```

If you pass a "callable" (Class/function) as a dependency in FastAPI, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a path operation function. Including sub-dependencies.

In some cases you don't really need the return value of a dependency inside your path operation function or the dependency doesn't return a value. But you still need it to be executed/solved. For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of dependencies to the path operation decorator.

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

For some types of applications you might want to add dependencies to the whole application. Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application. In that case, they will be applied to all the path operations in the application:

```python
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
```

### Middleware

A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.

It takes each request that comes to your application.
It can then do something to that request or run any needed code.
Then it passes the request to be processed by the rest of the application (by some path operation).
It then takes the response generated by the application (by some path operation).
It can do something to that response or run any needed code.
Then it returns the response.

```python
import time
from fastapi import FastAPI, Request
app = FastAPI()
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Extras

For SQL database management using FastAPI refer to [FastAPI SQL database Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/).
