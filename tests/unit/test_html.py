from pathlib import Path

import pytest

from actwise.ingest.html import html_string_to_text, html_to_text

RAW = Path(__file__).parents[2] / "data" / "raw"


def test_drops_noise_and_nbsp():
    html = """
    <html><head><script>var x = 1;</script><style>p {}</style></head>
    <body><nav>Menu</nav><p>Article&nbsp;6</p><footer>Legal notice</footer></body></html>
    """
    text = html_string_to_text(html)

    assert "Article 6" in text
    for noise in ["var x", "p {}", "Menu", "Legal notice"]:
        assert noise not in text


@pytest.mark.parametrize(
    ("filename", "annex_heading"),
    [
        ("ai_act.en.html", "ANNEX III"),
        ("ai_act.fr.html", "ANNEXE III"),
    ],
)
def test_saved_ai_act_pages_are_readable(filename, annex_heading):
    text = html_to_text(RAW / filename)

    assert "Article 6" in text
    assert annex_heading in text


@pytest.mark.parametrize("filename", ["gdpr.en.html", "gdpr.fr.html"])
def test_saved_gdpr_pages_are_readable(filename):
    text = html_to_text(RAW / filename)

    assert "Article 17" in text
