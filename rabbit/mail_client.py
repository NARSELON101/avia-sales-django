import smtplib

from config import SMTP_PASSWORD, SMTP_USERNAME, SMTP_SERVER


def send_message(to_email, subject, message_):
    message = ('From: %s\nTo: %s\nSubject: %s\n\n%s' % (SMTP_USERNAME,
                                                        to_email,
                                                        subject,
                                                        message_))

    mail_pass = SMTP_PASSWORD
    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    print(server.login(SMTP_USERNAME, mail_pass))
    server.auth_plain()
    server.sendmail(SMTP_USERNAME, to_email, message)


send_message(SMTP_USERNAME, "test", f"Hello http://127.0.0.1:8000")
