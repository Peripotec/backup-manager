import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

class NotificationService:
    @staticmethod
    def send_email(subject: str, body: str, to_emails: list[str] = None):
        """
        Envía un correo electrónico utilizando la configuración SMTP definida en settings.
        Soporta conexiones con y sin autenticación (si SMTP_PASSWORD está vacío).
        """
        if not settings.SMTP_SERVER:
            logging.warning("SMTP Configuration not set (SMTP_SERVER). Skipping email.")
            return

        # Use default recipients from settings if not provided
        if not to_emails:
            if not settings.SMTP_RECIPIENTS:
                logging.warning("No recipients defined. Skipping email.")
                return
            to_emails = [email.strip() for email in settings.SMTP_RECIPIENTS.split(",")]

        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            # Conexión inicial
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            
            # Lógica de seguridad y autenticación
            # Si hay password, asumimos que se requiere autenticación y posiblemente STARTTLS (común en puerto 587)
            if settings.SMTP_PASSWORD:
                if settings.SMTP_PORT != 25: # STARTTLS es raro en puerto 25 para redes internas, pero estándar en 587
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            
            # Envío
            text = msg.as_string()
            server.sendmail(settings.SMTP_FROM_EMAIL, to_emails, text)
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

        # Envío usando los destinatarios por defecto de la configuración
        NotificationService.send_email(subject, body)
