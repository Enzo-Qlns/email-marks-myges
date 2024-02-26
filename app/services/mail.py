import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

from config import settings

class mail:
    
    def __init__(self) -> None:
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD

    def generate_notification_email(self, is_exam, grade_updates):
        email_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Notification de nouvelles notes""" + "(exam)" if is_exam is True else "" + """</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }
                    .container {
                        max-width: 600px;
                        margin: 5px auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    h2 {
                        color: #333;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    ul li {
                        margin-bottom: 10px;
                    }
                    strong {
                        color: #007bff;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Notification de nouvelles notes""" + "(exam)" if is_exam is True else "" + """</h2>
                    <ul>
            """

        for course in grade_updates:
            for course_name, grades in course.items():
                for grade in grades:
                    email_content += f"""
                        <li><strong>Matière :</strong> {course_name}</li>
                        <li><strong>Nouvelle note :</strong> {grade}</li>
                    """
            
        email_content += """
                    </ul>
                </div>
            </body>
            </html>
        """
        return email_content

    def send_marks_email(self, is_exam, to, grade_updates):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Nouvelle note"

        body = self.generate_notification_email(
            is_exam=is_exam,
            grade_updates=grade_updates
        )
        msg.attach(MIMEText(body, 'html'))

        # Configurez votre serveur SMTP
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)

        # Envoyez l'email
        server.sendmail(self.smtp_username, [to], msg.as_string())
        print("mail envoyé")

        # Déconnectez-vous du serveur SMTP
        server.quit()