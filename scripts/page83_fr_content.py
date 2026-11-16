#!/usr/bin/env python3
"""French reader-facing copy for xindun-power news page 83 (not HTML-fragment MT)."""

from __future__ import annotations

ARTICLES = [
    {
        "source_url": "https://www.xindun-power.com/industry-news/Common-faults-of-solar-inverters-and-their-solutions.html",
        "title_en": "Common faults of solar inverters and their solutions.",
        "title_fr": "Pannes courantes des onduleurs solaires et leurs solutions",
        "seo_title_fr": "Pannes courantes des onduleurs solaires et leurs solutions",
        "description_fr": (
            "Après une utilisation prolongée, les onduleurs solaires présentent inévitablement "
            "quelques pannes mineures. Connaître les pannes courantes et leurs solutions vous "
            "évitera bien des soucis."
        ),
        "alt_fr": "Pannes courantes des onduleurs solaires et leurs solutions",
        "title_img_fr": "Pannes courantes des onduleurs solaires et leurs solutions",
        "body_html": """
<p>De nombreux foyers et bureaux disposent d’onduleurs solaires pour assurer une alimentation continue des appareils électriques importants tout au long de la journée. Comme toute machine, un onduleur solaire peut parfois tomber en panne. Si vous connaissez quelques pannes courantes et mineures ainsi que leurs solutions, vous vous éviterez bien des soucis. Nous présentons ci-dessous trois pannes fréquentes des onduleurs solaires et leurs solutions.</p>
<p>1. L’onduleur ne démarre pas.</p>
<p>L’impossibilité de mettre l’onduleur en marche est l’une des pannes les plus fréquentes. Une défaillance de l’interrupteur d’alimentation, un déclenchement de l’onduleur, une batterie non raccordée, des bornes de batterie desserrées, une batterie trop faible, des bornes inversées, etc. peuvent provoquer cette situation. Pour y remédier, il faut traiter la cause exacte. Si l’interrupteur d’alimentation est défaillant, il faut l’envoyer dans un centre de réparation ; si l’onduleur a déclenché, utilisez le bouton de réarmement prévu sur l’appareil ; si la batterie est trop faible, il est recommandé de la recharger pendant plusieurs heures ; si les bornes de la batterie sont desserrées, vérifiez leur corrosion et nettoyez-les bien avant de les resserrer.</p>
<p style="text-align:center;">{img0}</p>
<p>2. Le temps de secours est raccourci.</p>
<p>Cette situation peut venir d’une consommation électrique excessive : il faut alors retirer les charges supplémentaires. Par ailleurs, le temps de secours peut diminuer si la batterie perd de l’électrolyte. Il faut alors compléter régulièrement la batterie avec de l’eau distillée. Attention : le niveau d’eau doit rester compris entre les niveaux maximal et minimal.</p>
<p>3. L’alarme sonne en continu.</p>
<p>Lorsque l’alarme de l’onduleur bippe en continu, la cause possible est une surcharge de l’onduleur ou un ventilateur de refroidissement bloqué. En cas de surcharge, débranchez toutes les charges supplémentaires. Si le problème persiste, l’onduleur doit être confié à un technicien de maintenance. Chaque onduleur solaire possède un ventilateur de refroidissement, qui doit fonctionner tant que l’appareil est en marche. Si le ventilateur ne peut plus garantir un fonctionnement sûr, l’onduleur s’arrête automatiquement ou l’alarme se déclenche. De même, si le ventilateur est coincé et ne peut plus refroidir l’onduleur, l’appareil émet une alarme pour vous indiquer qu’il faut l’arrêter.</p>
<p>Pour toute autre question sur l’onduleur, contactez Xindun.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/How-long-is-the-service-life-of-the-photovoltaic-inverter.html",
        "title_en": "How long is the service life of the photovoltaic inverter?",
        "title_fr": "Quelle est la durée de vie de l’onduleur photovoltaïque ?",
        "seo_title_fr": "Quelle est la durée de vie de l’onduleur photovoltaïque ?",
        "description_fr": (
            "L’onduleur photovoltaïque se compose de pièces structurelles, de cartes électroniques, "
            "de dispositifs de puissance (IGBT ou MOS), de condensateurs, d’inductances et de "
            "transformateurs, de capteurs de courant, d’écrans LCD, de ventilateurs et d’autres "
            "composants. Sa durée de vie dépend de nombreux facteurs."
        ),
        "alt_fr": "Onduleur photovoltaïque",
        "title_img_fr": "Onduleur photovoltaïque",
        "body_html": """
<p>L’onduleur photovoltaïque se compose de pièces structurelles, de cartes électroniques, de dispositifs de puissance (IGBT ou MOS), de condensateurs, d’inductances et de transformateurs, de capteurs de courant, d’écrans LCD, de ventilateurs et d’autres composants. La durée de vie d’un onduleur photovoltaïque suit le « principe du tonneau » : elle est déterminée par le composant dont la durée de vie est la plus courte.</p>
<p>Dans un onduleur photovoltaïque, le composant à la durée de vie la plus courte est le condensateur électrolytique. Ce condensateur contient un électrolyte. Avec le temps, l’électrolyte peut s’évaporer et se dessécher, ce qui augmente l’impédance série équivalente (ESR) du condensateur. À courant identique, une ESR plus élevée fait chauffer le condensateur, ce qui accélère encore l’évaporation de l’électrolyte : un cercle vicieux se forme, jusqu’à la défaillance du composant.</p>
<p style="text-align:center;">{img0}</p>
<p>1. La température. Pour chaque hausse de 10 °C, la durée de vie du condensateur électrolytique est divisée par deux. Une température élevée accélère aussi le vieillissement optique du coupleur optoélectronique ; la défaillance de celui-ci peut endommager l’IGBT.</p>
<p>2. Les fonctions de protection et la CEM de l’onduleur. Si la protection et la conception CEM de l’onduleur sont insuffisantes, il sera facilement perturbé par l’environnement. Si la commande de l’IGBT est perturbée, elle peut conduire à une conduction intempestive et provoquer une explosion.</p>
<p>3. L’environnement d’installation. Les onduleurs photovoltaïques installés en plein soleil, dans un milieu très humide ou à pH élevé voient leur durée de vie réduite.</p>
<p>Dès lors que les composants sont bien choisis et que la conception est soignée, l’onduleur photovoltaïque peut fonctionner de façon stable pendant au moins 10 ans : il faut donc choisir une marque de qualité. Les onduleurs photovoltaïques Xindun Power protègent vos appareils électriques.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/improve-the-power-generation-efficiency-of-photovoltaic-systems.html",
        "title_en": "How to improve the power generation efficiency of photovoltaic systems?",
        "title_fr": "Comment améliorer le rendement de production des systèmes photovoltaïques ?",
        "seo_title_fr": "Comment améliorer le rendement de production des systèmes photovoltaïques ?",
        "description_fr": (
            "La capacité de production d’un système photovoltaïque dépend de nombreux facteurs : "
            "comment maximiser la production d’électricité d’un système photovoltaïque ?"
        ),
        "alt_fr": "Systèmes photovoltaïques",
        "title_img_fr": "Systèmes photovoltaïques",
        "body_html": """
<p>On pense généralement que l’ensoleillement est directement proportionnel à la production des systèmes photovoltaïques : plus le soleil est abondant, plus le système produit. C’est vrai, mais incomplet. La capacité de production d’un système photovoltaïque dépend de nombreux facteurs.</p>
<p>Les clients appellent souvent pour demander : en été, le soleil est fort et les journées sont longues, pourquoi la production des centrales photovoltaïques n’est-elle pas plus élevée qu’avant ? La raison la plus directe est la température. Un environnement trop chaud réduit le rendement des panneaux solaires et des onduleurs photovoltaïques.</p>
<p style="text-align:center;">{img0}</p>
<p>Comment alors maximiser la production des systèmes photovoltaïques ?</p>
<p>1. L’angle d’inclinaison du module photovoltaïque.</p>
<p>Quel est le meilleur angle d’inclinaison ? Les valeurs empiriques approximatives sont les suivantes :</p>
<p>Latitude 0° à 25° : l’inclinaison est égale à la latitude ; latitude 26° à 40° : l’inclinaison est égale à la latitude plus 5° à 10° ; latitude 41° à 55° : l’inclinaison est égale à la latitude plus 10° à 15°.</p>
<p>2. Le rendement de conversion photoélectrique des modules solaires.</p>
<p>Le rendement de conversion des panneaux solaires est un facteur clé de la production du système. La qualité des modules sur le marché est inégale. Lors du choix, ne vous arrêtez pas au prix le plus bas : tenez compte du rendement de conversion. Le rendement des modules en silicium polycristallin ne devrait pas être inférieur à 15,5 %, et celui des modules en silicium monocristallin ne devrait pas être inférieur à 16 %.</p>
<p>3. Le choix de l’onduleur.</p>
<p>L’onduleur est le composant central du système photovoltaïque, car le courant continu produit par le système doit être converti en courant alternatif avant d’alimenter les charges CA. Il faut choisir un onduleur à haut rendement de conversion, à haute sécurité et à faibles pertes.</p>
<p>4. La maintenance quotidienne du système photovoltaïque</p>
<p>Tâches principales : nettoyer à temps les saletés sur les panneaux solaires et remplacer sans délai les panneaux endommagés.</p>
<p>5. Un dimensionnement cohérent du système photovoltaïque.</p>
<p>Choisir les meilleurs accessoires ne suffit pas à construire un système photovoltaïque parfait. Un système haute performance passe par de nombreux essais et réglages : l’installation et le remplacement des pièces doivent donc être réalisés par des techniciens professionnels. Pour toute question sur un système photovoltaïque, vous pouvez contacter Guangdong Xindun Power Technology Co., Ltd.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/repairing-PV-inverter.html",
        "title_en": "What should we pay attention to when repairing PV inverter?",
        "title_fr": "À quoi faut-il prêter attention lors de la réparation d’un onduleur photovoltaïque ?",
        "seo_title_fr": "À quoi faut-il prêter attention lors de la réparation d’un onduleur photovoltaïque ?",
        "description_fr": (
            "Après une utilisation prolongée, l’onduleur photovoltaïque présente inévitablement "
            "quelques petites pannes. Les onduleurs PV sont des produits de puissance : la sécurité "
            "passe avant tout pendant la maintenance."
        ),
        "alt_fr": "Onduleur PV",
        "title_img_fr": "Onduleur PV",
        "body_html": """
<p>Après une utilisation prolongée, l’onduleur photovoltaïque présente inévitablement quelques petites pannes. Lors de la réparation, il faut prêter attention aux points suivants :</p>
<p>1. Mise hors tension : déconnecter l’onduleur du réseau, et déconnecter aussi les équipements du côté continu (CC).</p>
<p>2. Après la mise hors tension, attendre cinq à dix minutes que les composants internes se déchargent avant d’intervenir.</p>
<p>3. Les agents de maintenance doivent porter des gants isolants et un bracelet antistatique conformément aux consignes, éviter autant que possible le contact avec la carte électronique pendant l’intervention, et respecter les pictogrammes d’avertissement du produit.</p>
<p style="text-align:center;">{img0}</p>
<p>4. Le radiateur de l’onduleur photovoltaïque reste chaud pendant un certain temps après la coupure. Vérifier la température de surface avant d’intervenir pour éviter les brûlures. Veiller aussi aux autres risques de sécurité.</p>
<p>5. Après la réparation, s’assurer que tout défaut affectant la sécurité de l’onduleur a été éliminé, puis mettre l’onduleur photovoltaïque en marche.</p>
<p>Les onduleurs photovoltaïques sont des produits de puissance : la sécurité passe avant tout pendant la maintenance. Pour plus d’informations sur les onduleurs PV, contactez-nous.</p>
""".strip(),
    },
    {
        "source_url": "https://www.xindun-power.com/industry-news/inverter-OEM-service-manufacturer.html",
        "title_en": "Which manufacturer has better inverter OEM service?",
        "title_fr": "Quel fabricant propose le meilleur service OEM d’onduleurs ?",
        "seo_title_fr": "Quel fabricant propose le meilleur service OEM d’onduleurs ?",
        "description_fr": (
            "Xindun est un fabricant professionnel d’onduleurs en Chine, dispose d’un système OEM "
            "complet et peut personnaliser les produits selon les besoins des clients."
        ),
        "alt_fr": "Fabricant OEM d’onduleurs",
        "title_img_fr": "Fabricant OEM d’onduleurs",
        "body_html": """
<p>Xindun est un fabricant professionnel d’onduleurs en Chine, avec une équipe R&amp;D d’environ 20 personnes, plus de 100 opérateurs d’atelier, et une superficie d’atelier de plus de 6 000 m².</p>
<p style="text-align:center;">{img0}</p>
<p>Xindun dispose d’un système OEM complet et peut personnaliser les produits selon les besoins des clients. Au cours des 10 dernières années, le nombre de clients OEM en Chine et à l’étranger a dépassé 10 000. Les onduleurs commercialisés vont de 300 W à 160 kW, tous équipés de protections automatiques (surtension, sous-tension, surchauffe, surcharge, court-circuit) et d’une grande fiabilité ; un boîtier en fer de qualité et une carte électronique de haute précision, avec soudure séparée des composants enfichables et CMS, fournissent un courant de qualité ; un processeur haute performance assure une forte capacité de charge ; un ventilateur intelligent ajuste la vitesse selon la température interne pour une dissipation thermique plus efficace ; l’écran LCD affiche les données de fonctionnement de l’onduleur, parmi d’autres fonctions.</p>
<p>N’hésitez pas à nous appeler pour toute consultation !</p>
""".strip(),
    },
]


def prepend_18pt_title(body_html: str, title_fr: str) -> str:
    return f'<p><span style="font-size: 18pt;">{title_fr}</span></p>\n{body_html}'


def assert_no_translate_error(html: str) -> None:
    import re

    if re.search(r"Error\s*500|Server Error", html, re.I):
        raise RuntimeError("Google Translate Error 500/Server Error found in French content")
