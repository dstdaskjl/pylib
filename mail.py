import smtplib

class Mail:
    def send(self, sender, password, receiver, subject, message):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, receiver, 'Subject: {}\n\n{}'.format(subject, message))
            server.close()

        except Exception as e:
            print(str(e))

        finally:
            del server, sender, receiver, subject, message
