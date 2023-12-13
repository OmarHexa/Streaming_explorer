import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Load initial data
df = pd.DataFrame(columns=["id", "name", "email"])


class User(BaseModel):
    name: str
    email: str


@app.post("/users/", response_model=User)
async def create_user(user: User):
    """Create a new user and add it to the DataFrame.

    Args:
        user (User): User information provided in the request.

    Returns:
        JSONResponse: JSON response containing the created user.
    """
    user_dict = user.dict()
    user_dict["id"] = len(df) + 1
    df.loc[len(df)] = user_dict
    return JSONResponse(content=jsonable_encoder(user), status_code=201)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    """Read user information based on the provided user_id.

    Args:
        user_id (int): ID of the user to retrieve.

    Returns:
        JSONResponse: JSON response containing the user information.
    """
    user_data = df[df["id"] == user_id].to_dict(orient="records")
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=jsonable_encoder(user_data[0]))


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    """Update user information based on the provided user_id.

    Args:
        user_id (int): ID of the user to update.
        user (User): Updated user information provided in the request.

    Returns:
        JSONResponse: JSON response containing the updated user information.
    """
    user_data = df[df["id"] == user_id]
    if user_data.empty:
        raise HTTPException(status_code=404, detail="User not found")

    df.loc[df["id"] == user_id, ["name", "email"]] = [user.name, user.email]
    updated_user = df[df["id"] == user_id].to_dict(orient="records")[0]

    return JSONResponse(content=jsonable_encoder(updated_user))


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    """Delete user based on the provided user_id.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
        JSONResponse: JSON response containing the deleted user information.
    """
    user_data = df[df["id"] == user_id]
    if user_data.empty:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = user_data.to_dict(orient="records")[0]
    df.drop(df[df["id"] == user_id].index, inplace=True)

    return JSONResponse(content=jsonable_encoder(deleted_user))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
