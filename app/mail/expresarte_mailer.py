from flask_mail import Message, Mail
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import current_app, Flask
from app.config import Config

from app.mail.token_handler import MailTokenHandler

class ExpresarteMailer:
    def __init__(self, app: Flask=None):
        self.mail = Mail()
        if app:
            self.init_app(app)

        # Configurar entorno Jinja2 para plantillas de correo
        self.env = Environment(
            loader=FileSystemLoader("app/templates/mail"),
            autoescape=select_autoescape(["html", "xml"])
        )

    def init_app(self, app: Flask):
        """Inicializa Flask-Mail con la configuración de la app
        
        Args:
            app (Flask): Instancia de la aplicación Flask
        """
        try:
            self.mail.init_app(app)
            current_app.logger.debug("[ExpresarteMailer]: Inicializando Flask-Mail")
        except Exception as e:
            current_app.logger.error(f"[ExpresarteMailer]: Error al inicializar Flask-Mail: {e}")

    def render_template(self, template_name, **context):
        """Renderiza una plantilla Jinja2 con contexto
        
        Args:
            template_name (str): Nombre de la plantilla
            **context: Contexto para la plantilla
        
        Returns:
            str: Plantilla renderizada
        """
        try:
            template = self.env.get_template(template_name)
            current_app.logger.debug(f"[ExpresarteMailer]: Plantilla renderizada: {template}")
            return template.render(**context)
        except Exception as e:
            current_app.logger.error(f"[ExpresarteMailer]: Error al renderizar plantilla: {e}")
            return None

    def send_email(self, subject, recipients, template_name, context, sender=None) -> bool:
        """Envía un correo HTML usando una plantilla
        
        Args:
            subject (str): Asunto del correo
            recipients (list): Lista de destinatarios
            template_name (str): Nombre de la plantilla
            context (dict): Contexto para la plantilla
            sender (str, optional): Remitente del correo. Defaults to None.
        
        Returns:
            bool: True si el correo se envió correctamente, False en caso contrario
        """
        html_body = self.render_template(template_name, **context)
        sender = sender or current_app.config.get("MAIL_DEFAULT_SENDER")
        current_app.logger.debug(f"[ExpresarteMailer]: Sender: {sender}")

        try:
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=html_body,
                sender=sender
            )
            current_app.logger.debug(f"[ExpresarteMailer]: Correo enviado: {msg}")
            self.mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"[ExpresarteMailer]: Error al enviar correo: {e}")
            return False

    def send_reset_password(self, email: str, user_id: int):
        """Envía correo de recuperación de contraseña
        
        Args:
            email (str): Dirección de correo electrónico del usuario
            user_id (int): ID del usuario
        """
        token_handler = MailTokenHandler(user_id)
        token = token_handler.create_reset_token()
        reset_link = f"{current_app.config['APP_URL']}/auth/reset-password/{token}"
        
        current_app.logger.debug(f"[ExpresarteMailer]: Link de recuperación de contraseña: {reset_link}")
        
        self.send_email(
            subject="Recuperación de contraseña",
            recipients=[email],
            template_name="reset_password.html",
            context={"reset_link": reset_link}
        )
