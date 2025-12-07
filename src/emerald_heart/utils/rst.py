from __future__ import annotations

import logging

from docutils.core import publish_parts

LOG = logging.getLogger(__name__)


def rst_to_html(rst_text: str) -> str:
    """
    Convert text in RST form to html.

    Run the rst tool from docutils over the given string of text and make a few
    tweaks:

    - Remove the table border

    Optionally the text can be returned with the parent div stripped.
    """
    html_str = publish_parts(rst_text, writer_name="html")["html_body"]
    # We don't want the border=1 which docutils forces
    html_str = html_str.replace('<table border="1" class="docutils">', '<table class="docutils">')
    return html_str.strip()
