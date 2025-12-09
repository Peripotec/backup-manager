import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

class NotificationService:
    @staticmethod
    def send_email(subject: str, body: str, to_emails: list[str]):
        """
        Envía un correo electrónico utilizando la configuración SMTP definida en settings.
        """
        if not settings.SMTP_SERVER or not settings.SMTP_USER:
            logging.warning("SMTP not configured. Skipping email notification.")
            return

        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.SMTP_USER, to_emails, text)
            server.quit()
            logging.info(f"Email sent to {to_emails}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")

    @staticmethod
    def send_backup_report(success_count: int, failure_count: int, failures: list[dict]):
        """
        Genera y envía un reporte de backups.
        """
        subject = f"Backup Report: {success_count} Success, {failure_count} Failed"
        
        body = f"""
        <h1>Backup Execution Report</h1>
        <p><strong>Success:</strong> {success_count}</p>
        <p><strong>Failed:</strong> {failure_count}</p>
        """

        if failures:
            body += "<h2>Failures Detail</h2><ul>"
            for fail in failures:
                body += f"""
                <li>
                    <strong>{fail['device']}</strong>: {fail['error']}
                    <br>
                    <em>Diagnostic:</em> Ping: {'OK' if fail['diagnostic']['ping'] else 'FAIL'}
                </li>
                """
            body += "</ul>"

        # TODO: Get recipient list from settings or DB
        recipients = ["admin@example.com"] 
        NotificationService.send_email(subject, body, recipients)
