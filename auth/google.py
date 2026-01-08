# auth/google.py
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
load_dotenv()   # 👈 MUST be before os.getenv()
oauth = OAuth()
router = APIRouter()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/auth/google/login")
async def google_login(request: Request):

    return await oauth.google.authorize_redirect(
        request,
        os.getenv("GOOGLE_REDIRECT_URI")
    )

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    try:
        # Get the token from OAuth callback
        token = await oauth.google.authorize_access_token(request)
        
        # Fetch user info from Google using the token
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo', token=token)
        user_info = resp.json()
        
        # Extract email from user info
        email = user_info.get('email')
        
        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email not found in user information"
            )
        
        # Check if email domain is indoreinstitute.com
        email_parts = email.split('@')
        if len(email_parts) != 2:
            raise HTTPException(
                status_code=400,
                detail="Invalid email format"
            )
        
        email_domain = email_parts[1].lower()
        
        if email_domain != 'indoreinstitute.com':
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Only users with @indoreinstitute.com email addresses are allowed. Your email domain: {email_domain}"
            )
        
        # If domain is valid, proceed with authentication
        # Store user info in session
        request.session['user'] = {
            'email': email,
            'name': user_info.get('name')
        }
        
        # Redirect to frontend after successful authentication
        return RedirectResponse(url="http://iistfaceregister.vercel.app/upload_images")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}"
        )
