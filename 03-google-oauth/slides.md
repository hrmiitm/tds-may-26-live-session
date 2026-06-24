<div class="titlemark">TDS Web Apps • Topic 3</div>

# Google OAuth in FastAPI

Login with Google, create sessions, and allow or block users using a local database.

<span class="pill">OAuth</span><span class="pill">Session</span><span class="pill">Callback</span><span class="pill">Allowlist DB</span>

---

## Why OAuth?

<div class="flow">
  <span class="box">User</span><span class="arrow">→</span>
  <span class="box">Google proves identity</span><span class="arrow">→</span>
  <span class="box">Your app trusts verified email</span>
</div>

> Your app should not handle Google passwords. Google handles login; your app handles authorization.

---

## Authentication vs authorization

<div class="split">
<div class="card"><h3>Authentication</h3><p class="small">Who are you? Example: Google says this email is real.</p></div>
<div class="card"><h3>Authorization</h3><p class="small">Are you allowed here? Example: email exists in local allowlist.</p></div>
</div>

---

## OAuth flow

<div class="flow">
  <span class="box">/login</span><span class="arrow">→</span>
  <span class="box">Google consent</span><span class="arrow">→</span>
  <span class="box">/auth/callback</span><span class="arrow">→</span>
  <span class="box">Create session</span><span class="arrow">→</span>
  <span class="box">Protected route</span>
</div>

---

## Install

```bash
uv add fastapi uvicorn authlib itsdangerous sqlmodel
```

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="change-me")
```

---

## OAuth client setup

```python
from authlib.integrations.starlette_client import OAuth


oauth = OAuth()
oauth.register(
    name="google",
    client_id="GOOGLE_CLIENT_ID",
    client_secret="GOOGLE_CLIENT_SECRET",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
```

---

## Login route

```python
@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)
```

<p class="small">This sends the user to Google with your app’s callback URL.</p>

---

## Callback route

```python
@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    request.session["user"] = {
        "email": user["email"],
        "name": user.get("name"),
    }
    return {"message": "logged in", "user": request.session["user"]}
```

---

## Basic protected route

```python
def current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    return user

@app.get("/me")
def me(request: Request):
    return current_user(request)
```

---

## Local allow / disallow users

```python
ALLOWED_EMAILS = {
    "teacher@example.com",
    "student@example.com",
}

@app.get("/dashboard")
def dashboard(request: Request):
    user = current_user(request)
    if user["email"] not in ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Not allowed")
    return {"message": "welcome", "email": user["email"]}
```

---

## Replace allowlist with database

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select

class AllowedUser(SQLModel, table=True):
    email: str = Field(primary_key=True)
    active: bool = True

engine = create_engine("sqlite:///users.db")
SQLModel.metadata.create_all(engine)
```

---

## Check database permission

```python
def is_allowed(email: str) -> bool:
    with Session(engine) as session:
        row = session.exec(
            select(AllowedUser).where(AllowedUser.email == email)
        ).first()
        return bool(row and row.active)
```

---

## Logout

```python
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "logged out"}
```

<p class="small">Session cookie remains in browser, but server-side user data is cleared.</p>

---

## Security checklist

- Use HTTPS in production.
- Store secrets in environment variables.
- Restrict Google redirect URI exactly.
- Use strong session secret.
- Check email allowlist after login.
- Do not trust frontend-only checks.

---

## Practice

1. Create <code>/login</code>, <code>/me</code>, <code>/logout</code>.
2. Add SQLite allowlist table.
3. Add <code>/admin</code> route only for active allowed users.
4. Show a clear 403 for blocked users.

---

# Mental model

**Google confirms identity. Your database decides access. Session remembers the logged-in user.**
