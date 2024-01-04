from app.api_clients.users_client import UsersClient
from app.core.config import DOMAIN_MAPPER


def provide_users_client() -> UsersClient:
    return UsersClient(base_url=f"{DOMAIN_MAPPER['users']}/users/api/v1")
