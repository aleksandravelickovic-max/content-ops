"""Authentication routes using Google OAuth2.

Protects admin routes only. Review routes remain public (token-based access).
When GOOGLE_CLIENT_ID is not configured, admin access is unrestricted (dev mode).
"""

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    ALLOWED_DOMAINS,
    BASE_URL,
)

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="app/templates")

# --- OAuth setup ---

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


def is_oauth_configured() -> bool:
    """Return True when Google OAuth credentials are present."""
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def _email_domain_allowed(email: str) -> bool:
    """Check that the email belongs to an allowed domain."""
    if not email or "@" not in email:
        return False
    domain = email.rsplit("@", 1)[1].lower()
    return domain in ALLOWED_DOMAINS


# --- Routes ---


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str | None = None):
    """Show the login page, or redirect to Google if already clicked."""
    # If already authenticated, go straight to admin
    user = request.session.get("user")
    if user and _email_domain_allowed(user.get("email", "")):
        return RedirectResponse(url="/admin/", status_code=302)

    if not is_oauth_configured():
        return templates.TemplateResponse(request, "auth/login.html", {
            "error": error,
            "oauth_disabled": True,
        })

    return templates.TemplateResponse(request, "auth/login.html", {
        "error": error,
        "oauth_disabled": False,
    })


@router.get("/google")
async def google_login(request: Request):
    """Redirect to Google OAuth consent screen."""
    if not is_oauth_configured():
        return RedirectResponse(url="/auth/login?error=OAuth+not+configured", status_code=302)

    redirect_uri = f"{BASE_URL}/auth/callback"
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        hd="searchatlas.com",
    )


@router.get("/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback, validate domain, set session."""
    if not is_oauth_configured():
        return RedirectResponse(url="/auth/login?error=OAuth+not+configured", status_code=302)

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        return RedirectResponse(
            url="/auth/login?error=Authentication+failed.+Please+try+again.",
            status_code=302,
        )

    userinfo = token.get("userinfo")
    if not userinfo:
        return RedirectResponse(
            url="/auth/login?error=Could+not+retrieve+user+info+from+Google.",
            status_code=302,
        )

    email = userinfo.get("email", "")
    if not _email_domain_allowed(email):
        request.session.clear()
        domain = email.rsplit("@", 1)[1] if "@" in email else "unknown"
        return RedirectResponse(
            url=f"/auth/login?error=Access+denied.+%40{domain}+accounts+are+not+allowed.",
            status_code=302,
        )

    # Store user info in session
    request.session["user"] = {
        "email": email,
        "name": userinfo.get("name", ""),
        "picture": userinfo.get("picture", ""),
    }

    return RedirectResponse(url="/admin/", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    """Clear session and redirect to login."""
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)
