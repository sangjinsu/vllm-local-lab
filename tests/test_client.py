from vllm_lab.client import create_client
from vllm_lab.config import Settings


def test_create_client_uses_settings_base_url_and_api_key():
    client = create_client(
        Settings(
            vllm_base_url="http://localhost:9999/v1",
            vllm_api_key="EMPTY",
        )
    )

    assert str(client.base_url) == "http://localhost:9999/v1/"
    assert client.api_key == "EMPTY"
