import smtplib

class Mail:
    def send(self, host, port, sender, password, receiver, subject, message):
        try:
            server = smtplib.SMTP_SSL(host, port)
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, receiver, 'Subject: {}\n\n{}'.format(subject, message))
            server.close()

        except Exception as e:
            print(str(e))

        finally:
            del server, sender, receiver, subject, message

    def send_gmail(self, sender, password, receiver, subject, message):
        self.send('smtp.gmail.com', 465, sender, password, receiver, subject, message)
