from django.core.mail import send_mail


def send_letter(subject, message, recipients):
    send_mail(subject=subject, message=message,
              from_email="Ваше лисье величество <darklorian@darklorian.ru>", recipient_list=recipients)
