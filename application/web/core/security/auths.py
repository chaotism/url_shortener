from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from loguru import logger

from config import auth_config

AUTH_TOKEN_KEY = APIKeyHeader(
    name=auth_config.auth_token_key_name, auto_error=False
)  # set true for force checking token


def get_exists_auth_token_keys():
    return auth_config.tokens_list


async def verify_auth_token(
    auth_token: str = Depends(AUTH_TOKEN_KEY),
    valid_tokens: List[str] = Depends(get_exists_auth_token_keys),
) -> str:
    if valid_tokens:
        if (auth_token is None) or (auth_token not in valid_tokens):
            logger.warning(f'Bad token {auth_token}: cannot find this token in tokens')
            raise HTTPException(
                status_code=403, detail='Not authenticated: Invalid Auth-Token'
            )
    else:
        logger.warning(f'Empty auth tokens: {valid_tokens}')
    logger.info(f'Get access to {auth_token} token')
    return auth_token
