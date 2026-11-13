#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 66 (not HTML-fragment MT)."""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/faq/pwm-mppt-solar-controller.html",
        "title_en": "Is mppt solar controller really better than pwm solar controller?",
        "title_fr": "Le régulateur solaire MPPT est-il vraiment meilleur que le régulateur solaire PWM ?",
        "seo_title_fr": "Le régulateur solaire MPPT est-il vraiment meilleur que le régulateur solaire PWM ?",
        "description_fr": (
            "Il existe deux types de régulateurs solaires sur le marché : le régulateur solaire MPPT "
            "et le régulateur solaire PWM. Alors, quel régulateur solaire est le meilleur ?"
        ),
        "alt_fr": "Le régulateur solaire MPPT est-il vraiment meilleur que le régulateur solaire PWM ?",
        "title_img_fr": "Le régulateur solaire MPPT est-il vraiment meilleur que le régulateur solaire PWM ?",
        "body_html": """
<p>Le régulateur de charge solaire sert à réguler les processus de charge et de décharge dans un système solaire. Sa fonction principale est de contrôler le courant de charge qui circule du panneau photovoltaïque vers la batterie, et de maintenir ce courant à un niveau qui n’est pas trop élevé afin d’éviter la surcharge du parc de batteries. Il existe deux types de régulateurs solaires sur le marché : le régulateur solaire MPPT et le régulateur solaire PWM.</p>
<p>MPPT signifie Maximum Power Point Tracking (suivi du point de puissance maximale) : c’est une technologie qui suit et régule l’énergie fournie par les panneaux solaires vers les batteries. PWM est l’abréviation de Pulse Width Modulation (modulation de largeur d’impulsion) : c’est une technologie qui module la largeur d’impulsion selon des règles précises afin de modifier la tension et la fréquence de l’énergie fournie par le panneau solaire pour charger la batterie. Le régulateur MPPT offre un meilleur rendement de conversion (jusqu’à 99 %) et une charge en 3 étapes plus saine pour la batterie, mais son prix est élevé ; le régulateur PWM a une structure simple, une technologie mature et fiable, il est bon marché et rentable, mais son rendement de conversion est inférieur à celui du MPPT.</p>
<p style="text-align:center;">{img0}</p>
<p>Dans l’ensemble, le régulateur MPPT est effectivement meilleur que le PWM sur le plan fonctionnel. Mais « meilleur » et « adapté » sont deux concepts différents.</p>
<p>Quel régulateur de charge vous convient le mieux ?</p>
<p>Le régulateur de charge MPPT convient aux systèmes de production solaire de plus de 2 kW. Grâce à ses fonctions avancées, il peut vous faire économiser en réduisant d’autres coûts.</p>
<p>Le régulateur de charge PWM convient aux petits systèmes solaires hors réseau qui n’exigent pas beaucoup de fonctions et dont le budget est limité. Si vous souhaitez simplement un régulateur basique et économique pour un petit système d’éclairage, le régulateur PWM est le meilleur choix.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/inverter-peak-power-rated-power.html",
        "title_en": "What does the peak power of the power inverter mean and what is the difference between it and the rated power",
        "title_fr": "Que signifie la puissance de crête d’un onduleur et quelle est la différence avec la puissance nominale",
        "seo_title_fr": "Que signifie la puissance de crête d’un onduleur et quelle est la différence avec la puissance nominale",
        "description_fr": (
            "Lorsqu’il s’agit de déterminer la taille d’onduleur nécessaire, il faut distinguer "
            "la puissance nominale de la puissance de crête."
        ),
        "alt_fr": "Puissance de crête et puissance nominale de l’onduleur",
        "title_img_fr": "Puissance de crête et puissance nominale de l’onduleur",
        "body_html": """
<p>Lorsqu’il s’agit de déterminer de quelle taille d’onduleur de puissance on a besoin, il faut distinguer la puissance nominale de la puissance de crête.</p>
<p>La puissance de crête, aussi appelée puissance de pointe, est la puissance maximale que l’onduleur peut maintenir pendant une courte période (généralement moins de 20 ms) au démarrage. La puissance nominale, aussi appelée puissance de sortie continue, est une puissance stable et durable qui alimente votre charge en fonctionnement normal. Si la consommation totale de vos appareils électriques est de 1000 watts, vous avez besoin d’un onduleur dont la puissance nominale est de 1000 watts ou plus ; un onduleur de 1000 watts de crête et de 500 watts de puissance nominale ne convient pas dans ce cas.</p>
<p style="text-align:center;">{img0}</p>
<p>La puissance de crête est-elle un paramètre inutile ? Non.</p>
<p>La puissance de démarrage de certains appareils électriques est plusieurs fois supérieure à la puissance requise en fonctionnement normal, mais elle ne dure qu’un court instant. L’intérêt de la puissance de crête est de garantir que l’onduleur peut absorber ces pics et de protéger l’onduleur, afin d’éviter qu’un pic n’endommage l’appareil.</p>
<p>Les onduleurs de la série DP de Xindun, de 1 kW à 7 kW, ont une puissance de crête égale à trois fois la puissance nominale, ce qui leur permet de mieux gérer les pics électriques. N’hésitez pas à nous consulter.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/3-phase-50kw-photovoltaic-inverter.html",
        "title_en": "How much is the 380V AC output current of a 3 phase 50kw photovoltaic inverter",
        "title_fr": "Quel est le courant de sortie CA 380 V d’un onduleur photovoltaïque triphasé de 50 kW",
        "seo_title_fr": "Quel est le courant de sortie CA 380 V d’un onduleur photovoltaïque triphasé de 50 kW",
        "description_fr": (
            "D’après la formule P=UI, I=P/U, le courant de sortie CA 380 V d’un onduleur photovoltaïque "
            "triphasé de 50 kilowatts est égal à 50000 W / 380 V ≈ 131,6 A."
        ),
        "alt_fr": "Quel est le courant de sortie CA 380 V d’un onduleur photovoltaïque triphasé de 50 kW",
        "title_img_fr": "Quel est le courant de sortie CA 380 V d’un onduleur photovoltaïque triphasé de 50 kW",
        "body_html": """
<p>D’après la formule P=UI, I=P/U (où P est la puissance (W) ; U est la tension (V) ; I est le courant (A)), le courant de sortie CA 380 V d’un onduleur photovoltaïque triphasé de 50 kW est égal à 50 000 W / 380 V ≈ 131,6 A. Il s’agit d’un courant élevé : le courant de fonctionnement des appareils électroménagers quotidiens n’a pas besoin d’être aussi élevé.</p>
<p style="text-align:center;">{img0}</p>
<p>L’onduleur photovoltaïque triphasé 50 kW de Xindun délivre un courant alternatif 380 V à onde sinusoïdale pure. Il est largement utilisé dans les systèmes d’alimentation sans interruption dans les domaines militaire et des communications, ainsi que dans les usines et les entreprises. Cet onduleur est de type trois entrées / trois sorties, avec fonction de stabilisation de tension ; il peut s’adapter à un environnement de réseau difficile ; il supporte une charge triphasée déséquilibrée ; sa puissance de crête est égale à trois fois la puissance nominale, ce qui convient aux appareils équipés de moteurs.</p>
<p>En tant qu’entreprise d’onduleurs disposant de plus de 10 équipes techniques de R&amp;D et d’une usine de production de 6 000 m², Xindun peut fournir aux utilisateurs un accompagnement technique professionnel pour l’onduleur triphasé 50 kW, ainsi qu’un rapport qualité-prix plus avantageux pour l’onduleur 380 V. Si besoin, n’hésitez pas à nous consulter.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/home-inverter-single-phase.html",
        "title_en": "Is the home inverter single-phase or three-phase",
        "title_fr": "L’onduleur domestique est-il monophasé ou triphasé",
        "seo_title_fr": "L’onduleur domestique est-il monophasé ou triphasé",
        "description_fr": (
            "Si la charge est monophasée, l’onduleur utilisé pour alimenter cette charge est un onduleur monophasé. "
            "Les appareils électroménagers que nous utilisons sont généralement des charges monophasées, "
            "donc les onduleurs domestiques sont généralement monophasés."
        ),
        "alt_fr": "L’onduleur domestique est-il monophasé ou triphasé",
        "title_img_fr": "L’onduleur domestique est-il monophasé ou triphasé",
        "body_html": """
<p>La sortie d’un onduleur monophasé est un courant alternatif monophasé. Si la charge est monophasée, l’onduleur utilisé pour alimenter cette charge est un onduleur monophasé. La tension alternative convertie par un onduleur triphasé est triphasée, c’est-à-dire AC380V. L’alimentation triphasée se compose de trois potentiels alternatifs de même fréquence, de même amplitude, et décalés de 120° en phase. Si la charge est triphasée, l’onduleur utilisé pour alimenter cette charge est un onduleur triphasé. En général, les sources et les charges de courant alternatif utilisées dans l’industrie sont triphasées. Les appareils électroménagers que nous utilisons sont généralement des charges monophasées, donc les onduleurs domestiques sont généralement monophasés.</p>
<p style="text-align:center;">{img0}</p>
<p>Les onduleurs domestiques monophasés de la série WD de Xindun sont proposés à un prix raisonnable, avec une puissance de 700 W à 12 kW et une sortie à onde sinusoïdale pure, capables d’alimenter tous les appareils électriques du quotidien que le réseau peut alimenter. Xindun est un fabricant d’onduleurs domestiques monophasés avec plus de dix ans d’histoire. La qualité des produits est excellente, et les services avant-vente et après-vente sont de bon niveau. Si vous avez besoin d’un onduleur domestique monophasé, contactez-nous.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/faq/power-inverter-3000w-pure-sine-wave.html",
        "title_en": "How long can a 12V 75A battery with a 3000W pure sine wave power inverter drive a 40W refrigerator?",
        "title_fr": "Combien de temps une batterie 12 V 75 A avec un onduleur à onde sinusoïdale pure de 3000 W peut-elle alimenter un réfrigérateur de 40 W ?",
        "seo_title_fr": "Combien de temps une batterie 12 V 75 A avec un onduleur à onde sinusoïdale pure de 3000 W peut-elle alimenter un réfrigérateur de 40 W ?",
        "description_fr": (
            "Pour calculer combien de temps une batterie 12 V 75 Ah avec un onduleur à onde sinusoïdale pure "
            "de 3000 W peut alimenter un réfrigérateur de 40 W, il faut d’abord calculer le courant de "
            "fonctionnement du réfrigérateur, puis obtenir le résultat final selon la formule correspondante."
        ),
        "alt_fr": "Combien de temps une batterie 12 V 75 A avec un onduleur à onde sinusoïdale pure de 3000 W peut-elle alimenter un réfrigérateur de 40 W ?",
        "title_img_fr": "Combien de temps une batterie 12 V 75 A avec un onduleur à onde sinusoïdale pure de 3000 W peut-elle alimenter un réfrigérateur de 40 W ?",
        "body_html": """
<p>Pour calculer combien de temps une batterie 12 volts 75 ampères-heures avec un onduleur à onde sinusoïdale pure de 3000 W peut alimenter un réfrigérateur de 40 watts, il faut d’abord calculer le courant de fonctionnement du réfrigérateur. D’après I=P/U (tension du réseau), le courant du réfrigérateur = 40 W / 220 V ≈ 0,2 A. Durée d’alimentation = capacité de la batterie / courant du réfrigérateur = 75 Ah / 0,2 A = 375 h. En multipliant 375 h par le rendement de conversion de votre onduleur à onde sinusoïdale pure, on obtient le résultat final. Si le rendement de conversion de votre onduleur à onde sinusoïdale pure est très faible, la durée d’alimentation sera fortement réduite. Par conséquent, lors de l’achat d’un onduleur à onde sinusoïdale pure, il faut vérifier si son rendement de conversion est suffisamment élevé. Notre conseil : un onduleur à onde sinusoïdale pure dont le rendement de conversion est inférieur à 80 % n’a pas d’intérêt à l’achat.</p>
<p style="text-align:center;">{img0}</p>
<p>Les onduleurs à onde sinusoïdale pure de la série DP de Xindun présentent de faibles pertes, un haut rendement, un rendement de sortie d’onduleur ≥ 85 %, une fréquence de sortie stable et des fonctions de protection automatique complètes. Xindun est un fabricant officiel d’onduleurs à onde sinusoïdale pure, engagé dans la recherche, le développement, la production et la vente d’onduleurs à onde sinusoïdale pure. L’entreprise dispose d’excellentes équipes techniques, commerciales et après-vente. N’hésitez pas à nous consulter.</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
