#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 71 (not HTML-fragment MT)."""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/faq/Inverter-Choosing-Guide.html",
        "title_en": "Inverter Choosing  Guide",
        "title_fr": "Guide de choix d’un onduleur",
        "seo_title_fr": "Guide de choix d’un onduleur",
        "description_fr": (
            "Il y a de nombreux facteurs à prendre en compte pour choisir un onduleur, "
            "principalement le facteur de puissance, ainsi que le courant de crête en sortie, "
            "la tension d’entrée, le chargeur de batterie et le type de forme d’onde."
        ),
        "alt_fr": "Guide de choix d’un onduleur",
        "title_img_fr": "Guide de choix d’un onduleur",
        "body_html": """
<p>Un onduleur est un appareil qui convertit le courant continu en courant alternatif domestique standard. Les paramètres suivants vous aident à choisir le bon modèle : puissance nominale, tension d’entrée et de sortie, fréquence d’entrée, forme d’onde, rendement.</p>
<p style="text-align:center;">{img0}</p>
<p><strong>Puissance nominale :</strong> l’onduleur sert à alimenter des appareils, donc la puissance nominale se choisit d’après la puissance totale des appareils que vous voulez faire fonctionner.</p>
<p><strong>Tension d’entrée et de sortie :</strong> la tension d’entrée correspond à celle de la batterie qui fournit l’énergie, généralement 12 V, 24 V, 48 V, 96 V, 192 V, 220 V, 240 V ou 384 V. La tension de sortie suit la tension standard du pays.</p>
<p><strong>Fréquence d’entrée :</strong> 45 Hz–65 Hz. Les valeurs courantes sont 50 Hz ou 60 Hz.</p>
<p><strong>Forme d’onde :</strong> onde sinusoïdale pure, onde sinusoïdale modifiée et onde carrée. Un onduleur à onde sinusoïdale pure fournit un courant sinusoïdal propre et régulier : c’est le meilleur choix pour alimenter les appareils.</p>
<p><strong>Rendement :</strong> un rendement supérieur à 85 % est préférable.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/what-is-an-inverter.html",
        "title_en": "what is an inverter?",
        "title_fr": "Qu’est-ce qu’un onduleur ?",
        "seo_title_fr": "Qu’est-ce qu’un onduleur ?",
        "description_fr": (
            "L’onduleur est un appareil électrique qui convertit le courant continu (CC) en "
            "courant alternatif (CA). La tension d’entrée CC est généralement celle de la "
            "batterie ou du solaire, et la tension de sortie CA est la tension alternative "
            "domestique standard."
        ),
        "alt_fr": "Qu’est-ce qu’un onduleur ?",
        "title_img_fr": "Qu’est-ce qu’un onduleur ?",
        "body_html": """
<p>Un onduleur est un appareil électrique qui convertit une tension d’entrée en courant continu (CC) en une tension de sortie en courant alternatif (CA). La tension d’entrée CC est généralement celle d’une batterie ou d’une installation solaire, et la tension de sortie CA correspond à la tension alternative domestique standard. Il peut donc alimenter les appareils électroménagers courants.</p>
<p style="text-align:center;">{img0}</p>
<p>Il existe différents types d’onduleurs selon la forme d’onde de sortie, le nombre de phases et la fréquence. En général, on distingue deux grandes familles : l’onduleur hors réseau (off-grid) et l’onduleur raccordé au réseau (on-grid). L’onduleur hors réseau sert souvent d’alimentation de secours dans les zones où l’électricité manque, tandis que l’onduleur raccordé au réseau complète l’alimentation du réseau dans les régions développées.</p>
<p>En tant que fabricant d’onduleurs, nous nous concentrons depuis plus de 14 ans sur les onduleurs hors réseau. N’hésitez pas à nous contacter.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/Inverters-technical-performanc.html",
        "title_en": "Power inverter's technical performance (1)",
        "title_fr": "Performances techniques de l’onduleur de puissance (1)",
        "seo_title_fr": "Performances techniques de l’onduleur de puissance (1)",
        "description_fr": (
            "Les performances techniques de l’onduleur comprennent principalement la tension "
            "de sortie nominale, le déséquilibre de la tension de sortie et le rendement de "
            "sortie nominal. Voyons cela avec Xindun."
        ),
        "alt_fr": "Performances techniques de l’onduleur de puissance",
        "title_img_fr": "Performances techniques de l’onduleur de puissance",
        "body_html": """
<p>Performances techniques de l’onduleur de puissance :</p>
<p>1. Tension de sortie nominale : dans la plage de fluctuations autorisée de la tension d’entrée CC spécifiée, l’onduleur doit pouvoir délivrer la tension nominale. La précision de stabilité de la tension de sortie nominale est généralement spécifiée comme suit :</p>
<p>(1) En régime permanent, la plage de fluctuation de tension doit être limitée, par exemple un écart ne dépassant pas ± 3 % ou 5 % de la valeur nominale.</p>
<p>(2) L’écart de tension de sortie ne doit pas dépasser 8 % ou 10 % de la valeur nominale en régime dynamique lors d’une variation brusque de charge (charge nominale 0 % → 50 % → 100 %) ou d’autres facteurs de perturbation.</p>
<p>2. Déséquilibre de la tension de sortie : en conditions de fonctionnement normales, le déséquilibre des tensions triphasées de l’onduleur (rapport de la composante inverse à la composante directe) ne doit pas dépasser une valeur spécifiée, généralement exprimée en %, par exemple 5 % ou 8 %.</p>
<p style="text-align:center;">{img0}</p>
<p>3. Distorsion de la forme d’onde de la tension de sortie : lorsque la tension de sortie de l’onduleur est sinusoïdale, une distorsion maximale (ou un contenu harmonique) est autorisée. Elle s’exprime généralement par la distorsion totale de la forme d’onde de la tension de sortie et ne doit pas dépasser 5 % (10 % pour une sortie monophasée).</p>
<p>4. Fréquence de sortie nominale : la fréquence de la tension alternative en sortie de l’onduleur doit être une valeur relativement stable, généralement 50 Hz. En conditions normales, l’écart doit être inférieur à 1 %.</p>
<p>5. Facteur de puissance de la charge : il caractérise la capacité de l’onduleur à alimenter des charges inductives ou capacitives. En régime sinusoïdal, le facteur de puissance de la charge est de 0,7 à 0,9 (en retard), la valeur nominale étant 0,9.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/Solar-power-inverter-charger-wiring-diagram.html",
        "title_en": "Solar power inverter charger installation wiring diagram",
        "title_fr": "Schéma de câblage pour l’installation d’un onduleur-chargeur solaire",
        "seo_title_fr": "Schéma de câblage pour l’installation d’un onduleur-chargeur solaire",
        "description_fr": (
            "L’onduleur solaire génère du courant alternatif 110 V / 120 V / 220 V / 230 V, "
            "comme une prise domestique, ce qui peut menacer la vie. Il est important de "
            "l’installer et de le raccorder avec soin."
        ),
        "alt_fr": "Schéma de câblage pour l’installation d’un onduleur-chargeur solaire",
        "title_img_fr": "Schéma de câblage pour l’installation d’un onduleur-chargeur solaire",
        "body_html": """
<p>Voici d’abord quelques consignes de sécurité importantes : l’onduleur solaire génère du courant alternatif 110 V / 120 V / 220 V / 230 V, comme une prise domestique, ce qui peut menacer la vie. Il est essentiel de l’installer et de l’utiliser avec précaution.</p>
<p><strong>Étape 1 : Choisir un bon emplacement</strong></p>
<p>L’endroit où l’onduleur solaire est installé doit être aussi proche que possible de la batterie, dans un lieu sec et bien ventilé. Les onduleurs solaires muraux ont des trous de fixation : vous pouvez les visser au mur. Lors du choix de l’emplacement, veillez à ce que les bornes CC, les prises, les interrupteurs et les fusibles restent accessibles.</p>
<p><strong>Étape 2 : Raccorder la batterie</strong></p>
<p>Utilisez le câble fourni pour relier l’onduleur à la batterie. Il est possible de raccourcir les câbles, mais s’ils sont trop courts, il faut les remplacer par des câbles plus épais et plus longs.</p>
<p style="text-align:center;">{img0}</p>
<p><strong>Étape 3 : Mettre l’onduleur solaire à la terre</strong></p>
<p>La mise à la terre est très importante. Si l’onduleur solaire et vos équipements ne sont pas mis à la terre, un défaut peut mettre sous tension les appareils raccordés et l’onduleur. Si votre onduleur solaire possède un point de terre, utilisez un fil plus épais pour le relier à une terre adaptée.</p>
<p><strong>Étape 4 : Brancher un appareil de test</strong></p>
<p>Respectez la puissance nominale maximale de l’onduleur solaire, branchez l’appareil sur la prise CA de l’onduleur, puis allumez l’onduleur. Le voyant de mise sous tension doit s’allumer, et vous entendrez peut-être le ventilateur.</p>
<p>L’onduleur solaire mural Xindun LS a un faible encombrement et s’installe facilement. Si besoin, n’hésitez pas à nous consulter.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/Hybrid-inverter-for-rv-power-car-inverter.html",
        "title_en": "Hybrid inverter for rv and power car inverter",
        "title_fr": "Onduleur hybride pour camping-car et onduleur de voiture",
        "seo_title_fr": "Onduleur hybride pour camping-car et onduleur de voiture",
        "description_fr": (
            "Si vous souhaitez une alimentation de secours en courant alternatif pendant vos "
            "déplacements, vous pouvez acheter un onduleur embarqué et le raccorder à la "
            "batterie du véhicule, ou utiliser « panneau solaire + batterie + onduleur hybride » "
            "comme système de secours complet."
        ),
        "alt_fr": "Onduleur hybride pour camping-car et onduleur de voiture",
        "title_img_fr": "Onduleur hybride pour camping-car et onduleur de voiture",
        "body_html": """
<p>Un onduleur hybride est un appareil qui combine les fonctions d’onduleur et de régulateur solaire. Le régulateur solaire se place entre le panneau solaire et le parc de batteries : il contrôle l’énergie produite par le panneau qui entre dans la batterie, afin d’assurer une charge correcte et d’éviter la surcharge. Les onduleurs de voiture ordinaires n’ont pas de fonction de régulateur.</p>
<p>Si vous souhaitez une alimentation de secours en courant alternatif pendant vos voyages, vous pouvez acheter un onduleur de voiture et le raccorder à la batterie du véhicule : il convertit le courant continu de la batterie en courant alternatif. Veillez à ce que la capacité de la batterie du véhicule suffise à alimenter les appareils CA que vous voulez utiliser.</p>
<p style="text-align:center;">{img0}</p>
<p>Aujourd’hui, de nombreux propriétaires de camping-cars adoptent aussi le schéma « panneau solaire + batterie + onduleur hybride » comme système d’alimentation de secours complet, pour couvrir les besoins électriques en voyage en autonomie.</p>
<p>Le type d’alimentation de secours à privilégier dépend des préférences et des besoins de chacun. L’onduleur hybride Xindun série NB 500 W–40 kW, avec régulateur MPPT/PWM intégré, sortie à onde sinusoïdale pure, haute sécurité et qualité fiable ; l’onduleur de voiture série DP 1000 W–7000 W, sortie à onde sinusoïdale pure, écran externe en option pour surveiller facilement l’état de fonctionnement de l’onduleur à tout moment. N’hésitez pas à nous consulter.</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
