<div class="hero-center">
<div>
<div class="title-kicker">TDS • Authentication</div>
<h1>Google OAuth in FastAPI</h1>
<p class="big">Login with Google, verify identity, then allow/deny users from a local database.</p>
<p><span class="tag">OAuth</span><span class="tag">OIDC</span><span class="tag">session</span><span class="tag">allowlist</span></p>
</div>
</div>

---

## OAuth is delegated login

<div class="flow">
  <div class="node">User</div><div class="arrow">→</div>
  <div class="node">Your app</div><div class="arrow">→</div>
  <div class="node">Google login</div><div class="arrow">→</div>
  <div class="node">Callback</div><div class="arrow">→</div>
  <div class="node">Session</div>
</div>

<div class="callout">Your app does not handle the Google password. It asks Google: “Who is this user?”</div>

---

## Setup pieces

<div class="grid2">
<div class="card"><h3>Google Cloud Console</h3><p>OAuth client ID, client secret, authorized redirect URI.</p></div>
<div class="card"><h3>FastAPI app</h3><p>Routes for login, callback, logout, current user.</p></div>
</div>

```text
Redirect URI example:
http://localhost:8000/auth/callback
```

---

## Route design

```text
GET /                 public page
GET /login            redirect user to Google
GET /auth/callback    Google sends user back here
GET /me               protected route
POST /logout          clear session
```

<p class="muted">Keep authentication routes boring and predictable.</p>

---

## Session vs bearer token

<div class="grid2">
<div class="card"><h3>Session cookie</h3><p>Good for browser apps. Server remembers login data.</p></div>
<div class="card"><h3>Bearer token</h3><p>Good for APIs, mobile apps, and service-to-service calls.</p></div>
</div>

<div class="callout warn">For a beginner FastAPI + browser demo, session cookie is the simplest mental model.</div>

---

## Local DB controls access

<div class="flow">
  <div class="node">Google says<br>email verified</div><div class="arrow">→</div>
  <div class="node">Your DB checks<br>allowed?</div><div class="arrow">→</div>
  <div class="node">Allow / deny</div>
</div>

```python
ALLOWED_USERS = {
    "student1@example.com": {"role": "student"},
    "ta@example.com": {"role": "admin"},
}
```

---

## Install dependencies

```bash
pip install fastapi uvicorn authlib itsdangerous python-dotenv
```

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
```

---

## App + OAuth registration

```python
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
```

---

## Login + callback

```python
@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user["email"] not in ALLOWED_USERS:
        raise HTTPException(status_code=403, detail="Not allowed")
    request.session["user"] = dict(user)
    return RedirectResponse("/me")
```

---

## Protected route

```python
def require_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    return user

@app.get("/me")
def me(request: Request):
    user = require_user(request)
    return {"email": user["email"], "name": user.get("name")}
```

---

## Security mistakes to avoid

<ul class="checklist">
<li>Do not commit <strong>client secret</strong>.</li>
<li>Use HTTPS redirect URI in production.</li>
<li>Use a long random session secret.</li>
<li>Check <strong>email_verified</strong> when relying on email identity.</li>
<li>Do not treat Google login as role authorization; roles come from your DB.</li>
</ul>

---

## Teaching demo plan

<div class="grid3">
<div class="card"><div class="number">1</div><p>Public page with login button.</p></div>
<div class="card"><div class="number">2</div><p>Google callback stores session.</p></div>
<div class="card"><div class="number">3</div><p>Local DB allowlist denies unknown users.</p></div>
</div>
