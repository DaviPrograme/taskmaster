import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_alert(logfile, email, text):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    email_user = os.getenv('TASKMASTER_EMAIL')
    email_password = os.getenv('TASKMASTER_PASS')

    if not email_user or not email_password:
        print("ERROR: Unable to trigger email log alert as we did not find the 'TASKMASTER_EMAIL' and 'TASKMASTER_PASS' credentials in your environment")
        return

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email
    msg['Subject'] = 'Taskmaster Log Alert'

    corpo_email = f'A record was generated in the Taskmaster server log file that we believe you should be aware of.\nThe record was as follows:\n\n    "{text}"\n\nThe log file is attached to help with the analysis.\nAtt.,\n\nTaskmaster Team'
    msg.attach(MIMEText(corpo_email, 'plain'))
    arquivo = logfile

    try:
        with open(arquivo, 'rb') as f:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(f.read())
            encoders.encode_base64(parte)

            parte.add_header('Content-Disposition', f'attachment; filename={os.path.basename(arquivo)}')

            msg.attach(parte)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, msg['To'], msg.as_string())
        server.quit()
        print('INFO: Alert email sent successfully')
    except Exception as e:
        print(f'ERROR: Unable to send alert email: {e}')