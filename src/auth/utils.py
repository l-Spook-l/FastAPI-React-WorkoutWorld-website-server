from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
# from src.auth.models import User
from .models import User
from src.database import get_async_session

# ===================================================
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # для html файла
from email.message import EmailMessage  # просто для текст
from dotenv import load_dotenv
import os
import aiofiles
import aiosmtplib
from src.config import SMTP_USER_EMAIL, SMTP_PASSWORD


load_dotenv()
# ===================================================


# получаем пользователя
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def send_token_by_email(email, token):
    print('отправка работате')
    # Адрес электронной почты, которая будет отправлять сообщение
    sender = SMTP_USER_EMAIL

    # Адрес электронной почты, на который вы хотите отправить сообщение
    # recipient = email
    recipient = SMTP_USER_EMAIL

    # Это пароль для созданного приложения в почте
    password = SMTP_PASSWORD

    try:
        # Открывает и записываем страничку в - template
        async with aiofiles.open(f"src/auth/token.html", encoding='utf-8', mode='r') as file:
            template = await file.read()
            print('почтааааааааа', template)
    except IOError:
        print('почтааааааааа')
        return "The template"

    # message = MIMEMultipart("alternative")
    message = EmailMessage()

    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Тестовая тема"

    # message.attach(MIMEText(template, "html", "utf-8"))
    message.set_content(f"Hello, you have requested a password reset. Please follow the link to set a new password. "
                        f"If this wasn't you, please disregard this message <a>http://localhost:3000/reset-password/"
                        f"{token}</a>")

    await aiosmtplib.send(message, hostname="smtp.gmail.com", port=465, use_tls=True, username=sender,
                          password=password)

    print('Message sent successfully')
