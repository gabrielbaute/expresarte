import jwt
from typing import Optional, Union
from datetime import datetime, timedelta
from flask import current_app

from app.config import Config

class MailTokenHandler:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def create_reset_token(self) -> str:
        """Genera un token JWT para recuperación de contraseña"""
        expiration = timedelta(minutes=Config.RESET_TOKEN_EXP_MINUTES)
        payload = {
            'user_id': self.user_id,
            'exp': datetime.utcnow() + expiration
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        current_app.logger.debug(f"Token creado: {token}")
        return token

    @staticmethod
    def decode_token(token: str) -> Union[int, None]:
        """Decodifica el token y retorna el user_id si es válido"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_app.logger.debug(f"Token decodificado: {payload}")
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
