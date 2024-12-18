import requests


def send_ticket_email(ticket):
    url = "http://dax-ec.ru/api/enviar-email"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "id_number": ticket.id_number,
        "email": ticket.email
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Email enviado exitosamente")
    else:
        print(f"Error al enviar el email: {
              response.status_code} - {response.text}")
