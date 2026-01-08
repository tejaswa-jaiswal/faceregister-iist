from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import hmac
import hashlib
import time
import uuid
router = APIRouter()

@router.get("/imagekit-auth")
def imagekit_auth():
    """
    Generate ImageKit authentication parameters for client-side uploads.
    Returns token, expire, and signature.
    ImageKit expects this endpoint to return JSON with token, expire, and signature.
    """
    private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
    
    if not private_key:
        return JSONResponse(
            status_code=500,
            content={"error": "IMAGEKIT_PRIVATE_KEY not found in environment variables"}
        )
    
    # Generate token (current timestamp + 1 hour)
    now = int(time.time())

    expire = now + 600          # ✅ 5 minutes (SAFE)
    token = str(uuid.uuid4()) 
    
    # Generate signature using HMAC SHA1
    signature_string = f"{token}{expire}"
    signature = hmac.new(
        private_key.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    return JSONResponse(content={
        "token": token,
        "expire": expire,
        "signature": signature
    })