from fastapi import APIRouter

from models.mail import EmailModel
from mail.mail import mail, create_message

router = APIRouter()
@router.post('/send_mail/', tags=["Mail"])
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1> Welcome to Kizak! </h1>"

    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html
    )

    await mail.send_message(message)

    return {"message": "Email sent successfully"}
