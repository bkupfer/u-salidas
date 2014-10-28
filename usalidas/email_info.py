# -*- coding: utf-8 -*-
# for gmail.
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'salidas.dcc@gmail.com'
EMAIL_HOST_PASSWORD = 'no-escribire-la-password-aqui'
EMAIL_PORT = 587

# to send a mail :
# send_mail(subject, message, from_email, to_list, fail_silently = True)
#
# example:
#  subject = 'Nueva solicitud salidas Dcc'
#  message = 'El profesor {{ application.teacher }} ha enviado una nueva solicitud de salida.'
#  from_email = settings.EMAIL_HOST_USER
#  to_list = [save_it.email, email2@gmail.com]
#
#  send_mail(subject, message, from_email, to_list, fail_silently = True)

# example 2:
#  send_mail('Hola! Soy django!', 'Probando 123 probando :D yeeeii', settings.EMAIL_HOST_USER, ['bdokupferb@gmail.com'], fail_silently = False)

