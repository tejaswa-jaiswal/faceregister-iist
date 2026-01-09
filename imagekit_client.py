from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter,Request,Response
from fastapi.responses import JSONResponse
import os
import hmac
import hashlib
import time
import uuid
router = APIRouter()

@router.options("/imagekit-auth")
async def imagekit_auth_options():
    return Response(status_code=200)
@router.post("/imagekit-auth")
async def imagekit_auth(request: Request):
    # Disable any cache on server side
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
    if not private_key:
        return JSONResponse(status_code=500, content={"error": "IMAGEKIT_PRIVATE_KEY missing"}, headers=headers)

    now = int(time.time())
    expire = now + 600
    token = str(uuid.uuid4())
    signature = hmac.new(
        private_key.encode(),
        f"{token}{expire}".encode(),
        hashlib.sha1
    ).hexdigest()
    print("---------------------------------------------------------------------------")
    print(f"[ImageKit Auth] token: {token}, expire: {expire}, signature: {signature}")

    return JSONResponse(
        content={"token": token, "expire": expire, "signature": signature},
        headers=headers
    )