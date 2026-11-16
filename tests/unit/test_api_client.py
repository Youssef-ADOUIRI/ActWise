import httpx
import pytest

from actwise.integrations.client import ApiClient, ApiError


def api(handler, key=None):
    """A client whose requests go to `handler` instead of the network."""
    return ApiClient("http://api.test", key, transport=httpx.MockTransport(handler))


def test_post_sends_the_key_and_returns_the_json():
    """The path is joined to the URL, the key goes in X-API-Key, the JSON comes back."""
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"tier": "high_risk"})

    assert api(handler, key="secret").post("/classify", json={"description": "x"}) == {
        "tier": "high_risk"
    }
    assert str(seen[0].url) == "http://api.test/classify"
    assert seen[0].headers["X-API-Key"] == "secret"


def test_no_key_header_without_a_key():
    """A public API gets no X-API-Key header at all."""
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={})

    api(handler).post("/ask", json={})

    assert "X-API-Key" not in seen[0].headers


@pytest.mark.parametrize(
    ("response", "message"),
    [
        (httpx.Response(503, json={"detail": "no model answered"}), "503: no model answered"),
        (
            httpx.Response(422, json={"detail": [{"msg": "too short"}, {"msg": "too long"}]}),
            "422: too short; too long",
        ),
        (httpx.Response(502, text="Bad Gateway"), "502: Bad Gateway"),
    ],
)
def test_errors_carry_the_api_message(response, message):
    """FastAPI's detail, validation messages joined, or the raw body."""
    with pytest.raises(ApiError, match=message):
        api(lambda request: response).post("/ask", json={})


def test_an_unreachable_api_is_an_api_error():
    """A connection failure names the URL instead of raising httpx's error."""

    def handler(request):
        raise httpx.ConnectError("refused")

    with pytest.raises(ApiError, match="http://api.test did not answer"):
        api(handler).post("/ask", json={})


def test_from_env_reads_the_url_and_key():
    """ACTWISE_API_URL and ACTWISE_API_KEY, or localhost and no key."""
    configured = ApiClient.from_env(
        {"ACTWISE_API_URL": "https://x.run.app", "ACTWISE_API_KEY": "k"}
    )
    default = ApiClient.from_env({})

    assert (configured.url, configured.http.headers["X-API-Key"]) == ("https://x.run.app", "k")
    assert default.url == "http://localhost:8000" and "X-API-Key" not in default.http.headers
