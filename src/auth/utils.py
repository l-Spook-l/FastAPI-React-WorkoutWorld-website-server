from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from src.database import get_async_session
from email.message import EmailMessage  # просто для текста
from dotenv import load_dotenv
import aiosmtplib
from src.config import SMTP_USER_EMAIL, SMTP_PASSWORD

load_dotenv()


# получаем пользователя
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def send_token_by_email(email, token):
    print('отправка работает')
    # Адрес электронной почты, которая будет отправлять сообщение
    sender = SMTP_USER_EMAIL

    # Адрес электронной почты, на который вы хотите отправить сообщение
    # recipient = email
    recipient = SMTP_USER_EMAIL

    # Это пароль для созданного приложения в почте
    password = SMTP_PASSWORD

    message = EmailMessage()

    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Тестовая тема"

    message.set_content(f"Hello, you have requested a password reset. Please follow the link to set a new password. "
                        f"If this wasn't you, please disregard this message http://localhost:3000/reset-password/"
                        f"{token}")

    await aiosmtplib.send(message, hostname="smtp.gmail.com", port=465, use_tls=True, username=sender,
                          password=password)


async def send_message_to_admin(name, email, user_message):
    sender = SMTP_USER_EMAIL
    recipient = SMTP_USER_EMAIL
    password = SMTP_PASSWORD
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "User send email"
    message.set_content(f"This user {name}, his email {email}, send  message :{user_message}")

    await aiosmtplib.send(message, hostname="smtp.gmail.com", port=465, use_tls=True, username=sender,
                          password=password)
