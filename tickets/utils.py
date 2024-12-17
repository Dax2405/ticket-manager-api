import qrcode
from django.core.mail import EmailMessage
from io import BytesIO
from django.core.files.base import ContentFile


def send_ticket_email(ticket):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket.id_number)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = ContentFile(buffer.getvalue(), f"{ticket.id_number}.png")

    email = EmailMessage(
        'Tu Ticket',
        f'Aquí está tu ticket con ID: {ticket.id_number}',
        'nexalink@dax-ec.ru',
        [ticket.email],
    )
    email.attach(f"{ticket.id_number}.png", buffer.getvalue(), 'image/png')
    email.send()
