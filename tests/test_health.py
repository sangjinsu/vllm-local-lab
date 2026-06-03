from vllm_lab.config import Settings
from vllm_lab.health import check_health, server_root


def test_server_root_removes_v1_suffix():
    assert server_root("http://localhost:8000/v1") == "http://localhost:8000"


def test_check_health_returns_failure_for_connection_error(monkeypatch):
    def raise_error(*args, **kwargs):
        import requests

        raise requests.ConnectionError("no server")

    monkeypatch.setattr("vllm_lab.health.requests.get", raise_error)

    result = check_health(Settings(vllm_base_url="http://localhost:8000/v1"))

    assert result.ok is False
    assert result.status_code is None
    assert "연결할 수 없습니다" in result.message
