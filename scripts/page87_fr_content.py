#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 87 (not HTML-fragment MT).

Page 87 is the last listing page and contains 1 article.
"""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/industry-news/difference-between-inverter-and-hybrid-inverter.html",
        "title_en": "The difference between inverter and hybrid inverter",
        "title_fr": "La différence entre un onduleur et un onduleur hybride",
        "seo_title_fr": "La différence entre un onduleur et un onduleur hybride",
        "description_fr": (
            "Les onduleurs classiques et les onduleurs hybrides disposent tous d’une ou plusieurs "
            "batteries pour stocker l’énergie du système solaire ou du réseau lorsque l’électricité "
            "est disponible. L’onduleur hybride intègre une carte de régulateur photovoltaïque."
        ),
        "alt_fr": "Onduleur",
        "title_img_fr": "Onduleur",
        "body_html": """
<p>L’onduleur dispose en principe d’une ou plusieurs batteries pour stocker l’énergie issue du solaire ou du réseau lorsque l’électricité est disponible. Lorsque l’énergie solaire est insuffisante ou que le réseau est coupé, il convertit l’énergie stockée dans la batterie en électricité pour alimenter les charges CA.</p>
<p>Un onduleur classique ne peut être utilisé qu’en le raccordant à des batteries, et les onduleurs dotés d’une fonction de charge complémentaire peuvent servir d’alimentations UPS. Il peut aussi être utilisé dans un système de production solaire, mais un régulateur photovoltaïque de capacité adaptée est alors nécessaire entre le module photovoltaïque et la batterie.</p>
<p style="text-align:center;">{img0}</p>
<p style="text-align:center;">△ Schéma de l’onduleur</p>
<p>L’onduleur hybride est une version améliorée de l’onduleur. Il combine les fonctions d’un onduleur et d’un régulateur photovoltaïque. Il est généralement utilisé dans les systèmes de production solaire et n’a besoin d’être raccordé qu’aux modules photovoltaïques et aux batteries, ce qui réduit les coûts d’emballage et de transport des régulateurs photovoltaïques externes. Il est aussi plus simple à installer et plus compact, mais cela augmente la difficulté de maintenance.</p>
<p style="text-align:center;">{img1}</p>
<p style="text-align:center;">△ Schéma de l’onduleur hybride</p>
<p>L’utilisateur doit-il choisir un onduleur classique ou un onduleur hybride ? Selon ses préférences ou ses besoins, chacun a ses avantages.</p>
<p>Vous ne savez pas comment choisir un onduleur et un régulateur photovoltaïque ? Contactez Xindun Power pour des solutions d’énergie solaire gratuites.</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
