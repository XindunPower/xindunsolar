#!/usr/bin/env python3
"""Prepare page 29 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for English marketing headlines and product-card captions.
Factory floors, floating-panel photos, exhibition collages and plain product
lineups are compressed only. Product casing text, logos and wall company names
stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 29

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, "
    "product casing text, model numbers, display readings, Chinese characters, certificates, "
    "exhibition booth signs, or the URL xindun-power.com. "
    "Do not change words printed on the product such as ALL IN ONE SOLAR GENERATOR, "
    "SOLAR GENERATOR, STORAGE Power Inverter, HYBRID SOLAR INVERTER, or ATTENTION."
)

_SA_HERO = (
    "Marketing banner: solar array and two men in white thobes on the left, a blue headline panel "
    "and a blue APPLY button on the right. Translate only the overlay. Keep two headline lines and the button. "
    "Line 1 'Renewable Energy' → 'Возобновляемая энергия'. "
    "Line 2 'Solar Energy In Saudi Arabia' → 'Солнечная энергия в Саудовской Аравии'. "
    "Button 'APPLY' → 'ЗАЯВКА'. Keep the logo. " + _KEEP
)

_SA_FACTORY = (
    "Split marketing banner: orange and green headline on the left, a factory aisle photo on the right. "
    "Translate only the headline. Keep four lines. "
    "Line 1 'XINDUN power' stays in Latin letters 'XINDUN power'. "
    "Line 2 'manufacturer-' → 'производитель —'. "
    "Line 3 'solar inverter' → 'солнечный инвертор'. "
    "Line 4 'in Saudi Arabia' → 'в Саудовской Аравии'. "
    "Keep the orange URL badge xindun-power.com and the logo. " + _KEEP
)

_UAE = (
    "Marketing banner: a solar plant on the left and a white panel on the right. "
    "Translate only the green headline. Keep three lines. "
    "Line 1 'Current situation' → 'Текущее положение'. "
    "Line 2 'of Solar Energy' → 'солнечной энергетики'. "
    "Line 3 'in UAE' → 'в ОАЭ'. "
    "Keep the logo and the URL xindun-power.com. " + _KEEP
)

_KSA_SKY = (
    "Aerial photo of a solar field with one white headline across the sky. "
    "Translate only that headline. Keep it one line. "
    "'KSA with rich solar resources' → 'КСА с богатыми солнечными ресурсами'. " + _KEEP
)

_KSA_PRICE = (
    "Product marketing banner: three inverter cabinets on the left, a sunset field behind, "
    "a white headline on the right. Translate only the three headline lines. Keep three lines. "
    "Line 1 'Get the best' → 'Лучшая цена'. "
    "Line 2 'KSA solar' → 'солнечного инвертора'. "
    "Line 3 'inverter price' → 'в КСА'. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or any text on the cabinets. Keep the logo. " + _KEEP
)

_CUSTOMERS = (
    "Two exhibition photos side by side with one white caption along the bottom. "
    "Translate only that bottom caption. Keep two lines. "
    "Line 1 'Xindun looks forward to collaborating with customers' → 'Xindun ждёт сотрудничества с клиентами'. "
    "Line 2 'from around the world' → 'со всего мира'. "
    "Keep the brand word Xindun in Latin letters. "
    "Do NOT change booth banners, Chinese exhibition signs, hall numbers, NEW PRODUCT text, "
    "or words printed on the products. " + _KEEP
)

_EGYPT = (
    "Marketing banner: sunset panels on top, a dark blue lower band with arrows, the Egypt flag "
    "and a yellow headline. Translate only the yellow English headline. Keep it one line. "
    "'Egypt Solar PV Market' → 'Рынок солнечной фотоэлектрики Египта'. "
    "Keep the Arabic line under the headline unchanged. Keep the flag, arrows, logo and xindun-power.com. " + _KEEP
)

_VS = (
    "Three-column comparison card on a dark green background. Translate only the three white titles. "
    "'On Grid' → 'Сетевой'. 'Off Grid' → 'Автономный'. 'Hybrid Solar' → 'Гибридный'. "
    "Keep the red VS letters in Latin. "
    "Do NOT change STORAGE, Power Inverter, or any text printed on the three units. " + _KEEP
)

_SPEC = (
    "Product sheet with two product photographs on top and a caption block underneath. "
    "Do not change the photographs, the two-column layout, the green bar or the bullet dots. "
    "Keep the numeric specification line of watts and voltages exactly as printed. "
    "Translate only the product title under the photos and the three green bullet lines. "
)


def _card(title_en: str, title_ru: str, bullets: list[tuple[str, str]], extra: str = "") -> str:
    lines = [
        _SPEC,
        f"Title '{title_en}' → '{title_ru}'.",
    ]
    for src, dst in bullets:
        lines.append(f"Bullet '{src}' → '{dst}'.")
    if extra:
        lines.append(extra)
    lines.append(_KEEP)
    return " ".join(lines)


_LS = _card(
    "LS Off Grid Inverter",
    "Автономный инвертор LS",
    [
        ("Pure sine wave output, safe and stable", "Чистая синусоида, безопасно и стабильно"),
        ("Compatible with various inductive loads", "Совместим с индуктивной нагрузкой"),
        ("Intelligent control data, real-time monitoring", "Умный контроль и мониторинг в реальном времени"),
    ],
)

_ES = _card(
    "ES On Grid Inverter",
    "Сетевой инвертор ES",
    [
        ("A variety of intelligent modes can be set", "Можно задать разные умные режимы"),
        ("Reduce grid pressure and maximize profits", "Снижает нагрузку на сеть и повышает выгоду"),
        ("Dual MPPT input, efficient use of PV energy", "Два входа MPPT, эффективное использование PV"),
    ],
    "Do NOT change STORAGE Power Inverter printed on the unit.",
)

_HPT = _card(
    "HP PRO-T Solar Inverter",
    "Солнечный инвертор HP PRO-T",
    [
        ("High efficiency and low no-load loss", "Высокий КПД и малые потери холостого хода"),
        ("Built-in MPPT controller", "Встроенный контроллер MPPT"),
        ("Solar charging and mains complement design", "Заряд от солнца и дополнение от сети"),
    ],
    "Do NOT change HYBRID SOLAR INVERTER, CE or ATTENTION printed on the unit.",
)

_HP = _card(
    "HP PRO Hybrid Inverter",
    "Гибридный инвертор HP PRO",
    [
        ("Pure sine wave output", "Выход чистой синусоиды"),
        ("AC first, battery first, PV first", "Сначала сеть, аккумулятор или PV"),
        ("Extra wide voltage and frequency input range", "Очень широкий диапазон напряжения и частоты"),
    ],
)

_ESS = _card(
    "ESS Hybrid Inverter",
    "Гибридный инвертор ESS",
    [
        ("3 times peak power", "Пиковая мощность в 3 раза"),
        ("Combine inverter/solar controller/battery", "Инвертор, контроллер и аккумулятор вместе"),
        ("Monitor real-time work situations", "Контроль работы в реальном времени"),
    ],
    "Do NOT change ALL IN ONE SOLAR GENERATOR printed on the cabinet.",
)

_HDSX = _card(
    "HDSX Off Grid Inverter",
    "Автономный инвертор HDSX",
    [
        ("100% imbalance loading,3 times peak power", "100% несимметрия нагрузки, пик в 3 раза"),
        ("Built-in PWM or MPPT charge controller", "Встроенный контроллер заряда PWM или MPPT"),
        ("Remote monitoring RS485/APP(WIFI/GPRS)", "Удалённый контроль RS485/APP (WIFI/GPRS)"),
    ],
    "Keep RS485, APP, WIFI, GPRS, PWM and MPPT in Latin letters.",
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "sa_hero": "https://www.xindun-power.com/uploadfile/2023/03/11/202303111620146497.jpg",
    "sa_factory": "https://www.xindun-power.com/uploadfile/2023/03/11/202303111622092145.jpg",
    "uae": "https://www.xindun-power.com/uploadfile/2023/04/14/202304140907251715.jpg",
    "uae_float": "https://www.xindun-power.com/uploadfile/2023/04/14/202304140910299598.jpg",
    "uae_building": "https://www.xindun-power.com/uploadfile/2023/04/14/202304140914164208.jpg",
    "ksa_sky": "https://www.xindun-power.com/uploadfile/2023/04/04/202304041749452342.jpg",
    "ksa_price": "https://www.xindun-power.com/uploadfile/2023/04/07/202304071019361413.jpg",
    "ksa_customers": "https://www.xindun-power.com/uploadfile/2023/04/04/202304041752469726.jpg",
    "egypt": "https://www.xindun-power.com/uploadfile/2023/02/24/202302241051389894.jpg",
    "egypt_factory": "https://www.xindun-power.com/uploadfile/2023/07/10/202307101601316460.jpg",
    "vs": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202110703vsBcnl.jpg",
    "lineup": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202111151MhCjq9.jpg",
    "show": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202111427xtByKV.jpg",
    "ls": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202111529VF1B4g.jpg",
    "es": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021115297aV8Hg.jpg",
    "hpt": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202111607yxtwvU.jpg",
    "hp": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202111609gr4cQa.jpg",
    "ess": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021116100XhVRK.jpg",
    "hdsx": "https://www.xindun-power.com/uploadfile/2023/12/02/2023120211161128Urhw.jpg",
}

DUOMI_BY_URL = {
    U["sa_hero"]: _SA_HERO,
    U["sa_factory"]: _SA_FACTORY,
    U["uae"]: _UAE,
    U["ksa_sky"]: _KSA_SKY,
    U["ksa_price"]: _KSA_PRICE,
    U["ksa_customers"]: _CUSTOMERS,
    U["egypt"]: _EGYPT,
    U["vs"]: _VS,
    U["ls"]: _LS,
    U["es"]: _ES,
    U["hpt"]: _HPT,
    U["hp"]: _HP,
    U["ess"]: _ESS,
    U["hdsx"]: _HDSX,
}

IMAGE_SOURCES = [
    [
        _im(U["sa_hero"], "Лучший солнечный инвертор в Саудовской Аравии"),
        _im(U["sa_factory"], "Солнечный инвертор в Саудовской Аравии"),
    ],
    [
        _im(U["uae"], "Текущее положение солнечной энергетики в ОАЭ"),
        _im(U["uae_float"], "Перспективы солнечной энергетики в ОАЭ: плавучие солнечные панели"),
        _im(U["uae_building"], "China Xindun Power — сильная солнечная компания"),
    ],
    [
        _im(U["ksa_sky"], "КСА с богатыми солнечными ресурсами: цена солнечного инвертора в КСА"),
        _im(U["ksa_price"], "Цена солнечного инвертора в КСА"),
        _im(U["ksa_customers"], "Клиенты со всего мира сотрудничают с Xindun Power"),
    ],
    [
        _im(U["egypt"], "Анализ рынка солнечной фотоэлектрики Египта"),
        _im(U["egypt_factory"], "China Xindun Power: анализ рынка фотоэлектрики Египта"),
    ],
    [
        _im(U["vs"], "Сетевой, автономный и гибридный солнечный инвертор"),
        _im(U["lineup"], "Автономный, гибридный, солнечный и обычный инвертор"),
        _im(U["show"], "Завод обычных инверторов Xindun Power"),
        _im(U["ls"], "Автономный инвертор серии LS"),
        _im(U["es"], "Сетевой и гибридный инвертор серии ES"),
        _im(U["hpt"], "Солнечный гибридный инвертор серии HP PRO-T"),
        _im(U["hp"], "Обычный инвертор серии HP PRO"),
        _im(U["ess"], "Гибридный инвертор серии ESS"),
        _im(U["hdsx"], "Автономный инвертор серии HDSX"),
    ],
]

IMAGE_LOG = engine.IMAGE_LOG


def prepare_all():
    engine.PAGE_NUM = PAGE_NUM
    engine.DUOMI_BY_URL = DUOMI_BY_URL
    engine.IMAGE_SOURCES = IMAGE_SOURCES
    engine.IMAGE_LOG.clear()
    return engine.prepare_all()


if __name__ == "__main__":
    import json

    prepare_all()
    print(json.dumps(IMAGE_LOG, ensure_ascii=False, indent=2))
