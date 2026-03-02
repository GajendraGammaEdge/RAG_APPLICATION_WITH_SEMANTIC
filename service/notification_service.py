from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
from db_configuration.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_sender,
    MAIL_PASSWORD=settings.smtp_password,
    MAIL_FROM=settings.smtp_sender,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_server,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=True,   
    MAIL_SSL_TLS=False    
)

async def sending_mail(subject: str, email_to: str, body: dict):
    template_path = "templeate/mail.html"
    
    with open(template_path, "r") as f:
        template = Template(f.read())
    
    html_content = template.render(body=body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype="html",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        print(f"Mail sent successfully to {email_to}")
    except Exception as e:
        print(f"Error sending email: {e}")