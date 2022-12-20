"""Config of auth"""
from typing import List, Optional

from pydantic import BaseSettings, Field

AUTH_TOKEN_KEY_NAME = 'Auth-Token'


class AuthSettings(BaseSettings):
    auth_token_key_name: str = AUTH_TOKEN_KEY_NAME
    tokens: str = Field('', env='TOKENS')
    tokens_list: Optional[List[str]] = []

    @classmethod
    def generate(cls):
        base_settings = cls()
        raw_tokens = base_settings.tokens
        if not raw_tokens:
            return base_settings
        if ',' in raw_tokens:
            tokens_list = raw_tokens.split(',')
        elif r'\n' in raw_tokens:
            tokens_list = raw_tokens.split(r'\n')
        else:
            tokens_list = raw_tokens.split(' ')
        return cls(tokens_list=tokens_list)
