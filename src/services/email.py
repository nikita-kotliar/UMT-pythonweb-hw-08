from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors

from src.conf.config import settings
from src.services.auth import create_email_token

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)


async def send_verification_email(email: str, username: str) -> None:
    token = create_email_token({"sub": email})
    verify_url = f"{settings.BASE_URL}/auth/verify/{token}"

    message = MessageSchema(
        subject="Verify your email – Contacts API",
        recipients=[email],
        body=(
            f"<h2>Hello, {username}!</h2>"
            f"<p>Please verify your email address by clicking the link below:</p>"
            f'<p><a href="{verify_url}">{verify_url}</a></p>'
            f"<p>The link is valid for 24 hours.</p>"
        ),
        subtype=MessageType.html,
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        print(f"[Email] Verification email sent to {email}")
    except ConnectionErrors as err:
        print(f"[Email] ConnectionError: {err}")
    except Exception as err:
        print(f"[Email] Unexpected error: {type(err).__name__}: {err}")
