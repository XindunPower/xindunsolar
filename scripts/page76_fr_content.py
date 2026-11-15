#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 76 (not HTML-fragment MT)."""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/industry-news/square-wave-inverter.html",
        "title_en": "Why can't square wave inverter carry inductive load?",
        "title_fr": "Pourquoi un onduleur à onde carrée ne peut-il pas alimenter une charge inductive ?",
        "seo_title_fr": "Pourquoi un onduleur à onde carrée ne peut-il pas alimenter une charge inductive ?",
        "description_fr": (
            "L’onduleur à onde carrée fournit un courant alternatif en onde carrée de mauvaise "
            "qualité, inadapté aux charges inductives. Pour alimenter une charge inductive, "
            "choisissez un onduleur à onde sinusoïdale pure."
        ),
        "alt_fr": "Pourquoi un onduleur à onde carrée ne peut-il pas alimenter une charge inductive ?",
        "title_img_fr": "Pourquoi un onduleur à onde carrée ne peut-il pas alimenter une charge inductive ?",
        "body_html": """
<p>À strictement parler, les onduleurs à onde carrée ne sont pas incapables d’alimenter des charges inductives : ils sont simplement inadaptés à ce type de charge. Une charge inductive est une charge qui présente des paramètres inductifs. La valeur de crête de la tension de force contre-électromotrice générée à l’instant de la mise sous ou hors tension est bien supérieure au seuil de l’alimentation alternative de la charge, ce qui peut facilement provoquer une surcharge instantanée de l’onduleur et affecter sa durée de vie. C’est pourquoi une charge inductive impose des exigences relativement élevées à la forme d’onde de l’onduleur. L’onduleur à onde carrée fournit un courant alternatif en onde carrée de mauvaise qualité : ses crêtes positive et négative apparaissent presque simultanément, ce qui endommagerait fortement la charge et l’onduleur lui-même s’il était forcé d’alimenter une charge inductive.</p>
<p>Si vous devez alimenter une charge inductive, vous pouvez choisir un onduleur dont la forme d’onde est une sinusoïde pure. L’onduleur à onde sinusoïdale pure délivre un courant alternatif pur, identique à celui du réseau, capable d’alimenter les charges que le réseau peut alimenter. La puissance des onduleurs produits par Xindun va de 300 W à 200 kW, tous en sortie onde sinusoïdale pure. Pour toute question, contactez-nous.</p>
<p style="text-align:center;">{img0}</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/square-modified-pure-sine-wave-inverter.html",
        "title_en": "Pure sine wave inverter vs. square wave inverter vs modified sine wave",
        "title_fr": "Onduleur à onde sinusoïdale pure vs onduleur à onde carrée vs onde sinusoïdale modifiée",
        "seo_title_fr": "Onduleur à onde sinusoïdale pure vs onduleur à onde carrée vs onde sinusoïdale modifiée",
        "description_fr": (
            "Les onduleurs se répartissent principalement en trois catégories selon la forme d’onde : "
            "onduleur à onde sinusoïdale pure, onduleur à onde sinusoïdale modifiée et onduleur à "
            "onde carrée. Cet article présente brièvement les différences entre ces trois types."
        ),
        "alt_fr": "Onduleur à onde sinusoïdale pure vs onduleur à onde carrée vs onde sinusoïdale modifiée",
        "title_img_fr": "Onduleur à onde sinusoïdale pure vs onduleur à onde carrée vs onde sinusoïdale modifiée",
        "body_html": """
<p>Les onduleurs se répartissent principalement en trois catégories selon la forme d’onde : l’onduleur à onde sinusoïdale pure, l’onduleur à onde sinusoïdale modifiée et l’onduleur à onde carrée.</p>
<p>L’onduleur à onde carrée fournit un courant alternatif en onde carrée de mauvaise qualité : ses crêtes positive et négative apparaissent presque en même temps, ce qui endommage la charge et l’onduleur. De plus, sa capacité de charge est faible, environ la moitié de la puissance nominale seulement, et il ne peut pas alimenter de charges inductives.</p>
<p>Par rapport à l’onduleur à onde carrée, l’onduleur à onde sinusoïdale modifiée est un peu amélioré : ses crêtes positive et négative ne sont plus générées simultanément, mais avec un intervalle tampon. En réalité, l’onduleur à onde sinusoïdale modifiée appartient encore à la famille des onduleurs à onde carrée, car la forme d’onde qu’il produit reste composée de segments de droite, comme l’onde carrée, et sa continuité est médiocre.</p>
<p>L’onduleur à onde sinusoïdale pure fournit un courant alternatif de haute qualité, capable d’alimenter une grande variété de charges, sans pratiquement aucun dommage pour la charge ni pour l’onduleur. Bien que le coût des onduleurs à onde sinusoïdale pure soit plus élevé que celui des onduleurs à onde carrée et à onde sinusoïdale modifiée, nous recommandons tout de même de choisir autant que possible un onduleur à onde sinusoïdale pure.</p>
<p style="text-align:center;">{img0}</p>
<p>L’onduleur à onde sinusoïdale pure Xindun propose de nombreuses puissances, une grande stabilité et des protections complètes. En tant que fabricant établi d’onduleurs à onde sinusoïdale pure, Xindun assure un service avant-vente, en cours de vente et après-vente complet. N’hésitez pas à nous consulter.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/3000-watt-power-inverter-charger.html",
        "title_en": "How many batteries do I need for a 3000 watt power inverter charger?",
        "title_fr": "Combien de batteries faut-il pour un onduleur-chargeur de 3000 watts ?",
        "seo_title_fr": "Combien de batteries faut-il pour un onduleur-chargeur de 3000 watts ?",
        "description_fr": (
            "Pour équiper un onduleur de batteries, il faut tenir compte de la tension d’adaptation "
            "de l’onduleur, de la puissance totale consommée par les appareils électriques, etc."
        ),
        "alt_fr": "Combien de batteries faut-il pour un onduleur-chargeur de 3000 watts ?",
        "title_img_fr": "Combien de batteries faut-il pour un onduleur-chargeur de 3000 watts ?",
        "body_html": """
<p>Pour calculer le nombre de batteries nécessaires à un onduleur-chargeur de 3000 watts, on peut utiliser la formule : durée d’utilisation continue de l’équipement × puissance de l’équipement = puissance totale ; puissance totale / tension continue = ampérage requis.</p>
<p>Par exemple, si la puissance totale de vos appareils électriques est de 2000 watts, la durée d’utilisation continue de 3 heures et la tension de batterie de 12 V, alors 2000 W × 3 h = 6000 Wh, 6000 Wh / 12 V = 500 Ah : 500 Ah est l’ampérage requis. Cet algorithme vide complètement la batterie, et des décharges fréquentes jusqu’à épuisement raccourcissent sa durée de vie. En règle générale, nous recommandons une profondeur de décharge de 50 %, c’est-à-dire de diviser par 50 % le résultat obtenu avec cette formule pour choisir la capacité de batterie.</p>
<p style="text-align:center;">{img0}</p>
<p>En outre, pour équiper l’onduleur d’une batterie, il faut aussi choisir le nombre de batteries en fonction de la tension d’adaptation de l’onduleur : la tension continue de l’onduleur doit correspondre à la tension de la batterie. Pour toute question, contactez Xindun.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/12v-inverter-battery-last-with-generator-inverter.html",
        "title_en": "How long will a 12v pure sine wave inverter battery last with a pure sine wave power generator inverter?",
        "title_fr": "Combien de temps durera une batterie d’onduleur 12 V à onde sinusoïdale pure avec un onduleur-générateur à onde sinusoïdale pure ?",
        "seo_title_fr": "Combien de temps durera une batterie d’onduleur 12 V à onde sinusoïdale pure avec un onduleur-générateur à onde sinusoïdale pure ?",
        "description_fr": (
            "Le temps d’utilisation conjoint de la batterie 12 V à onde sinusoïdale pure et de "
            "l’onduleur dépend de la consommation de la charge, de la capacité de la batterie et "
            "de la capacité de l’onduleur à convertir le courant."
        ),
        "alt_fr": "Combien de temps durera une batterie d’onduleur 12 V à onde sinusoïdale pure avec un onduleur-générateur à onde sinusoïdale pure ?",
        "title_img_fr": "Combien de temps durera une batterie d’onduleur 12 V à onde sinusoïdale pure avec un onduleur-générateur à onde sinusoïdale pure ?",
        "body_html": """
<p>À vrai dire, on ne peut pas savoir très précisément combien de temps une batterie d’onduleur 12 V à onde sinusoïdale pure peut durer lorsqu’elle est utilisée avec l’onduleur. Car aucune batterie ne reste longtemps à 12 V : la tension n’est pas constante, on ne peut donc calculer qu’un temps approximatif.</p>
<p>Prenons l’exemple d’une batterie complètement déchargée (nous ne le recommandons pas, car cela raccourcit la durée de vie de la batterie) : si vous avez une batterie d’onduleur 12 V 100 Ah, et que la charge consomme 120 W / 12 V, soit 10 A, le temps d’utilisation de votre batterie est 100 Ah / 10 A = 10 heures. C’est le temps idéal en supposant un rendement de conversion de l’onduleur de 100 % ; or le rendement n’atteint pas 100 %, donc le temps réel sera de 8 à 9 heures.</p>
<p style="text-align:center;">{img0}</p>
<p>En général, le temps d’utilisation conjoint de la batterie 12 V à onde sinusoïdale pure et de l’onduleur dépend de la consommation de la charge, de la capacité de la batterie et de la capacité de l’onduleur à convertir le courant.</p>
<p>Pour toute question, n’hésitez pas à contacter Xindun : nous serons heureux de vous aider.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/transformer-in-DC-AC-converter-nverter.html",
        "title_en": "Which type of transformer is used in DC to AC converter and inverter?",
        "title_fr": "Quel type de transformateur est utilisé dans le convertisseur et l’onduleur CC-CA ?",
        "seo_title_fr": "Quel type de transformateur est utilisé dans le convertisseur et l’onduleur CC-CA ?",
        "description_fr": (
            "Un onduleur convertit le CC en CA, tandis qu’un transformateur est un appareil "
            "électrique qui utilise le principe de l’induction électromagnétique pour convertir "
            "l’énergie électrique. Le transformateur est une pièce très importante de l’onduleur."
        ),
        "alt_fr": "Quel type de transformateur est utilisé dans le convertisseur et l’onduleur CC-CA ?",
        "title_img_fr": "Quel type de transformateur est utilisé dans le convertisseur et l’onduleur CC-CA ?",
        "body_html": """
<p>L’onduleur convertit le courant continu en courant alternatif, tandis que le transformateur est un appareil électrique qui applique le principe de l’induction électromagnétique pour réaliser la conversion d’énergie. Il peut convertir une tension et un courant alternatifs en une autre tension et un autre courant alternatifs de même fréquence. Le transformateur est une pièce très importante de l’onduleur. L’onduleur convertit d’abord le courant continu en courant alternatif pulsé via les MOS, puis élève la tension grâce au transformateur, avant de passer par le pont en H pour achever tout le processus d’ondulation.</p>
<p>Le transformateur utilisé dans l’onduleur est un transformateur de puissance.</p>
<p>Selon la forme, on distingue le transformateur toroïdal, le transformateur en bande et le transformateur carré.</p>
<p style="text-align:center;">{img0}</p>
<p>Selon la fréquence, on distingue le transformateur à fréquence industrielle et le transformateur à noyau magnétique. Les onduleurs à fréquence industrielle utilisent des transformateurs à fréquence industrielle ordinaires, et les transformateurs à noyau magnétique sont destinés aux onduleurs haute fréquence.</p>
<p>Selon le nombre de phases, on distingue le transformateur monophasé et le transformateur triphasé. Le transformateur monophasé est un appareil statique ; il fonctionne selon le principe de la loi de Faraday sur l’induction mutuelle. Les transformateurs monophasés conviennent aux onduleurs monophasés. Les alimentations triphasées sont principalement utilisées pour la production, le transport et la distribution industriels. Un groupe de trois transformateurs monophasés connectés ensemble peut jouer le rôle d’un transformateur triphasé, ce qui coûte moins cher que d’acheter un transformateur triphasé seul. Les transformateurs triphasés conviennent aux onduleurs triphasés.</p>
<p>Pour toute question, contactez Xindun.</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
