"""OIC service implementation."""

from typing import TYPE_CHECKING

from src.domain.entities.token import Token
from src.domain.interfaces.oic import IOICService

if TYPE_CHECKING:
    from src.core.config._global import Config
    from src.domain.interfaces.oauth_provider import IOAuthProvider
    from src.domain.interfaces.storage_repository import IStorageRepository
    from src.domain.interfaces.token import ITokenService


class OICService(IOICService):
    def __init__(
        self,
        oauth_provider: "IOAuthProvider",
        token_service: "ITokenService",
        storage: "IStorageRepository",
        config: "Config",
    ):
        self.oauth_provider = oauth_provider
        self.token_service = token_service
        self.storage = storage
        self.config = config

    async def login(
        self,
        code: str | None,
        ip_address: str,
        code_verifier: str | None = None,
    ) -> Token:
        """Start the OIC flow."""

        token_data = await self.oauth_provider.exchange_code(
            code, code_verifier=code_verifier
        )
        user_info = await self.oauth_provider.get_user_info(
            token_data=token_data
        )
        jwt_access_token = self.token_service.create_access_token(user_info.id)
        jwt_refresh_token = self.token_service.create_refresh_token()

        await self.storage.create(
            user_info.id,
            jwt_refresh_token,
            ip_address,
            ttl=self.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        )

        return Token(
            access_token=jwt_access_token, refresh_token=jwt_refresh_token
        )
