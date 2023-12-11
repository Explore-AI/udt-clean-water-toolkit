from typing import Union



@app.get("/user")
def get_user():
    return {"bob"}
