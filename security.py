from authx import AuthX, AuthXConfig

config = AuthXConfig(
  JWT_SECRET_KEY="",
  JWT_TOKEN_LOCATION=["cookies"],
  JWT_ACCESS_COOKIE_NAME="access_token",
  JWT_COOKIE_CSRF_PROTECT=True,
  JWT_COOKIE_SECURE=True,
  JWT_COOKIE_HTTP_ONLY=True,
  JWT_COOKIE_SAMESITE="strict",
  JWT_CSRF_CHECK_FORM=True
)

security = AuthX(config=config)
