#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 72 (not HTML-fragment MT)."""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/industry-news/connect-off-grid-inverter-batteries.html",
        "title_en": "How do I connect two or more off grid inverter batteries",
        "title_fr": "Comment raccorder deux batteries ou plus à un onduleur hors réseau",
        "seo_title_fr": "Comment raccorder deux batteries ou plus à un onduleur hors réseau",
        "description_fr": (
            "Utiliser un onduleur et une batterie pour assurer une alimentation de secours à la "
            "maison est très courant. En cas de coupure, l’onduleur convertit le courant continu "
            "de la batterie en courant alternatif pour les appareils. Il existe deux façons de "
            "raccorder les batteries : série et parallèle."
        ),
        "alt_fr": "Comment raccorder deux batteries ou plus à un onduleur hors réseau",
        "title_img_fr": "Comment raccorder deux batteries ou plus à un onduleur hors réseau",
        "body_html": """
<p>Utiliser un onduleur associé à une batterie pour assurer une alimentation de secours à la maison est très courant. En cas de coupure de courant, l’onduleur convertit le courant continu de la batterie en courant alternatif pour alimenter les appareils électroménagers.</p>
<p>Il existe deux façons de raccorder les batteries à l’onduleur : en série et en parallèle. Si vous connectez deux batteries 12 V en série, la tension totale devient la somme des deux, soit 24 V. Si vous les connectez en parallèle, la tension totale reste celle d’une seule batterie, soit 12 V. Deux batteries en parallèle fournissent deux fois plus d’ampères-heures qu’une seule ; quatre batteries en fournissent quatre fois plus, et ainsi de suite. Cela allonge le temps de charge, mais aussi le temps pendant lequel vous pouvez faire fonctionner vos appareils.</p>
<p style="text-align:center;">{img0}</p>
<p><strong>Remarque :</strong> lors du raccordement de l’onduleur et de la batterie, ne jamais inverser les pôles positif et négatif.</p>
<p>Xindun Power est un fabricant fiable, spécialisé dans la production d’onduleurs et de batteries. Si vous en avez besoin, contactez-nous.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/battery-for-inverter-charger.html",
        "title_en": "How large is the battery for the 3000w inverter charger, and the total number of inverters and batteries",
        "title_fr": "Quelle capacité de batterie pour un onduleur-chargeur de 3000 W, et combien d’onduleurs et de batteries au total",
        "seo_title_fr": "Quelle capacité de batterie pour un onduleur-chargeur de 3000 W, et combien d’onduleurs et de batteries au total",
        "description_fr": (
            "Pour déterminer la taille de la batterie d’un onduleur de 3000 W, il faut d’abord "
            "connaître votre consommation électrique quotidienne, puis faire le calcul. En règle "
            "générale, plus la profondeur de décharge est faible, plus la durée de vie de la "
            "batterie est longue."
        ),
        "alt_fr": "Quelle capacité de batterie pour un onduleur-chargeur de 3000 W",
        "title_img_fr": "Quelle capacité de batterie pour un onduleur-chargeur de 3000 W",
        "body_html": """
<p>Pour déterminer la taille de la batterie d’un onduleur-chargeur de 3000 W, il faut d’abord connaître votre consommation électrique quotidienne, puis faire un calcul simple en suivant les étapes ci-dessous. En règle générale, plus la profondeur de décharge d’une batterie est faible, plus sa durée de vie est longue.</p>
<p><strong>Étape 1 :</strong> calculez votre consommation quotidienne (Wh) en additionnant la consommation de chaque appareil à alimenter. Vous pouvez l’obtenir en multipliant la puissance nominale de l’appareil par le nombre d’heures d’utilisation. Si l’appareil n’indique pas de puissance (watts), multipliez le courant en ampères (A) par la tension de fonctionnement (V). Exemple : un ensemble d’appareils d’une puissance totale de 3000 W utilisé 1 heure par jour = 3000 Wh par jour.</p>
<p><strong>Étape 2 :</strong> déterminez le nombre de jours d’autonomie souhaité, puis multipliez la consommation de l’étape 1 par ce nombre. Exemple, 2 jours de secours : 3000 × 2 = 6000 Wh.</p>
<p><strong>Étape 3 :</strong> comme indiqué plus haut, on décharge la batterie le moins possible pour allonger sa durée de vie. Choisissez une profondeur de décharge maximale (DOD), puis divisez le résultat de l’étape 2 par cette valeur. Exemple, DOD de 50 % : 6000 / 0,5 = 12 000 Wh.</p>
<p style="text-align:center;">{img0}</p>
<p><strong>Étape 4 :</strong> le rendement des batteries baisse à basse température ; on peut en tenir compte dans le calcul. Prenez le coefficient correspondant à la température moyenne la plus basse à laquelle la batterie fonctionnera, puis multipliez le résultat de l’étape 3 par ce coefficient. En supposant un coefficient de 1,05 : 4800 × 1,05 = 12 600 Wh.</p>
<p><strong>Étape 5 :</strong> selon la tension du système, raccordez les batteries pour constituer un parc 12 V, 24 V ou 48 V. Divisez le résultat de l’étape 4 par la tension du parc. Exemple : 12 600 / 12 = 1050 Ah.</p>
<p><strong>Étape 6 :</strong> déterminez le nombre de batteries nécessaires. Pour constituer un parc 12 V 1050 Ah avec des batteries 12 V 105 Ah, il en faut : 1050 / 105 = 10 pièces.</p>
<p>Voici la méthode de calcul théorique de « quelle batterie associer à un onduleur de 3000 W ». Si le calcul vous paraît complexe, ou si vous souhaitez une valeur plus directe de capacité et de quantité, contactez directement Xindun.</p>
<p>Onduleur à onde sinusoïdale pure Xindun série DP 3000 W : 18 kg ; batterie plomb-acide 7-250 Ah : 2,1-69 kg. Les poids varient selon le modèle d’onduleur et le type de batterie. Si besoin, demandez-nous des photos.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/pure-sine-wave-solar-inverter-charger.html",
        "title_en": "A pure sine wave solar inverter charger how does it work",
        "title_fr": "Comment fonctionne un onduleur-chargeur solaire à onde sinusoïdale pure",
        "seo_title_fr": "Comment fonctionne un onduleur-chargeur solaire à onde sinusoïdale pure",
        "description_fr": (
            "Un onduleur est un appareil électronique qui convertit le courant continu (CC) en "
            "courant alternatif (CA). L’onde sinusoïdale pure est une onde continue, forme "
            "d’onde idéale pour le transport du courant alternatif. Le fonctionnement d’un "
            "onduleur à onde sinusoïdale pure se déroule en trois étapes."
        ),
        "alt_fr": "Comment fonctionne un onduleur-chargeur solaire à onde sinusoïdale pure",
        "title_img_fr": "Comment fonctionne un onduleur-chargeur solaire à onde sinusoïdale pure",
        "body_html": """
<p>Un onduleur est un appareil électronique qui convertit le courant continu (CC) en courant alternatif (CA). L’onde sinusoïdale pure est une onde continue : elle décrit une oscillation répétitive et régulière, et constitue la forme d’onde idéale pour le transport du courant alternatif, avec une distorsion harmonique très faible.</p>
<p>Comment fonctionne un onduleur à onde sinusoïdale pure ? Son travail se déroule en trois étapes : l’oscillation, le boost ou l’amplification, et la transformation de sortie.</p>
<p><strong>Étape d’oscillation :</strong> l’onduleur génère des impulsions d’oscillation via un circuit intégré (IC) ; ces oscillations produisent des crêtes de tension positives et négatives alternées, à une fréquence déterminée.</p>
<p><strong>Étape de boost ou d’amplification :</strong> la tension alternative produite par l’oscillateur de l’onduleur à onde sinusoïdale pure est amplifiée à un niveau de courant élevé. L’électricité amplifiée est bien en alternatif, mais la tension reste très basse, encore au niveau de celle de la batterie.</p>
<p><strong>Étape du transformateur de sortie :</strong> dans un transformateur CA-CC, l’induction magnétique des deux enroulements abaisse la tension jusqu’au niveau alternatif voulu. Le transformateur d’un onduleur à onde sinusoïdale pure fonctionne de façon analogue, mais en sens inverse. Le courant alternatif de bas niveau issu de l’étage d’amplification est appliqué à l’enroulement secondaire du transformateur de sortie. Ce processus élève la tension, que l’onduleur utilise ensuite pour alimenter les appareils CA.</p>
<p style="text-align:center;">{img0}</p>
<p>La puissance fournie par un onduleur à onde sinusoïdale pure est égale ou supérieure à celle du réseau domestique. Il s’appuie sur une technologie élaborée pour protéger les appareils électroniques les plus sensibles, comme les fours à micro-ondes numériques, les téléviseurs, les réfrigérateurs, les ordinateurs portables, etc. Un onduleur à onde sinusoïdale pure peut alimenter presque n’importe quel appareil CA sans risque de dommages. De plus en plus de personnes l’utilisent. À noter : nous estimons qu’un onduleur à onde sinusoïdale pure dont le rendement de conversion est inférieur à 80 % n’a pas d’intérêt à l’achat.</p>
<p>Pour toute question sur les onduleurs à onde sinusoïdale pure, contactez Xindun.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/Use-of-off-grid-power-house-inverter.html",
        "title_en": "Use of off grid power house inverter",
        "title_fr": "Utilisation d’un onduleur hors réseau pour la maison",
        "seo_title_fr": "Utilisation d’un onduleur hors réseau pour la maison",
        "description_fr": (
            "L’onduleur de puissance convertit le courant continu de la batterie, généralement "
            "12 V / 24 V / 48 V, en courant alternatif classique 120 V / 220 V / 230 V. Cet "
            "article explique comment utiliser correctement l’onduleur de puissance."
        ),
        "alt_fr": "Utilisation d’un onduleur hors réseau pour la maison",
        "title_img_fr": "Utilisation d’un onduleur hors réseau pour la maison",
        "body_html": """
<p>L’onduleur de puissance convertit le courant continu de la batterie, généralement 12 V / 24 V / 48 V, en courant alternatif classique 120 V / 220 V / 230 V. Raccordez l’onduleur à la batterie pour obtenir une alimentation portable destinée aux appareils CA : climatiseurs, réfrigérateurs, téléviseurs, magnétoscopes, etc. Cet article explique comment utiliser correctement un onduleur hors réseau pour la maison.</p>
<p style="text-align:center;">{img0}</p>
<p>1. La tension d’entrée CC de l’onduleur doit être identique à celle de la batterie. Chaque onduleur accepte une tension continue donnée — 12 V, 24 V ou 48 V — qui doit correspondre à la tension de la batterie.</p>
<p>2. La puissance de sortie de l’onduleur doit être supérieure à la puissance totale des appareils que vous voulez faire fonctionner en même temps.</p>
<p>3. Les pôles positif et négatif de l’onduleur doivent être raccordés correctement. Les bornes de tension CC de l’onduleur sont marquées + et −, tout comme la batterie. On relie positif avec positif, négatif avec négatif.</p>
<p>3. Les pôles positif et négatif de l’onduleur doivent être raccordés correctement. Les bornes de tension CC de l’onduleur sont marquées + et −, tout comme la batterie. On relie positif avec positif, négatif avec négatif.</p>
<p>4. Placez l’onduleur dans un endroit bien ventilé, non humide, et à l’abri de la pluie. Laissez au moins 10 cm d’espace avec les objets environnants.</p>
<p>5. Ne démarrez pas trop fréquemment : laissez plus de 5 secondes entre deux mises en marche.</p>
<p>6. Avant de raccorder l’entrée et la sortie de l’onduleur, mettez correctement le boîtier à la terre.</p>
<p>7. Lorsque vous raccordez l’onduleur à la batterie, vérifiez qu’il n’y a pas de métal sur vos mains, afin d’éviter un court-circuit de la batterie et des brûlures.</p>
<p>Voici les précautions de base pour l’utilisation d’un onduleur de puissance. Pour plus d’informations, contactez-nous.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/Pwm-and-mppt-solar-controller.html",
        "title_en": "Pwm and mppt solar controller selection",
        "title_fr": "Choix d’un régulateur solaire PWM ou MPPT",
        "seo_title_fr": "Choix d’un régulateur solaire PWM ou MPPT",
        "description_fr": (
            "Si vous prévoyez d’installer un système solaire hors réseau avec un parc de "
            "batteries, vous avez besoin d’un régulateur de charge solaire. Ni le PWM ni le "
            "MPPT n’est intrinsèquement meilleur : le choix dépend de vos besoins."
        ),
        "alt_fr": "Choix d’un régulateur solaire PWM ou MPPT",
        "title_img_fr": "Choix d’un régulateur solaire PWM ou MPPT",
        "body_html": """
<p>Si vous prévoyez d’installer un système solaire hors réseau avec un parc de batteries, vous avez besoin d’un régulateur de charge solaire. C’est un appareil placé entre le panneau solaire et le parc de batteries, qui contrôle l’électricité produite par le panneau et envoyée vers la batterie. Sa fonction principale est d’assurer une charge correcte et d’éviter la surcharge.</p>
<p>Deux types de régulateurs de charge sont aujourd’hui couramment utilisés dans les systèmes photovoltaïques : 1. les régulateurs à modulation de largeur d’impulsion (PWM) ; 2. les régulateurs à suivi du point de puissance maximale (MPPT).</p>
<p><strong>Régulateur solaire PWM :</strong></p>
<p>Le PWM, ou modulation de largeur d’impulsion, est une méthode de régulation de la charge électrique. Il abaisse la tension du champ photovoltaïque jusqu’à une valeur proche de celle de la batterie, afin d’assurer une charge correcte. Il utilise un interrupteur électronique (MOSFET) pour connecter et déconnecter le panneau de la batterie. En commutant le MOSFET à haute fréquence avec différentes largeurs d’impulsion, on maintient une tension constante. Le régulateur PWM s’ajuste en faisant varier la largeur (la durée) et la fréquence des impulsions envoyées à la batterie.</p>
<p>Le régulateur PWM convient mieux aux petits systèmes solaires. C’est une solution économique, généralement utilisée lorsque la température des cellules solaires se situe entre 45 °C et 75 °C.</p>
<p style="text-align:center;">{img0}</p>
<p><strong>Régulateur solaire MPPT :</strong></p>
<p>Le régulateur de charge MPPT extrait le maximum de puissance du module photovoltaïque en le forçant à fonctionner à une tension proche du point de puissance maximale. Il est conçu pour ajuster sa tension d’entrée afin d’exploiter la puissance maximale du champ solaire, puis de convertir cette puissance pour répondre à des besoins de tension variables. La tension d’entrée est modifiée au moyen d’un convertisseur CC/CC.</p>
<p>Le régulateur MPPT s’appuie pour cela sur un algorithme adaptatif qui suit le point de puissance maximale du panneau ou du champ, puis ajuste la tension d’entrée pour conserver le rendement le plus efficace du système. Lorsque la température des cellules est basse (en dessous de 45 °C), l’avantage de performance du MPPT est très net. Ils sont plus efficaces que le régulateur PWM. Le régulateur MPPT est la meilleure solution pour les systèmes de forte puissance.</p>
<p>Aucun de ces deux régulateurs n’est intrinsèquement meilleur que l’autre : le choix dépend des besoins de chacun. Régulateur solaire PWM Xindun 10 A-200 A, régulateur solaire MPPT 10 A-100 A : n’hésitez pas à nous consulter.</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
