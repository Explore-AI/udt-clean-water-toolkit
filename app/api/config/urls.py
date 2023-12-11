from config.auth.backends import login_for_access_token

@app.get("/token")(login_for_access_token)
