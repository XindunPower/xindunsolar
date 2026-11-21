#!/usr/bin/env python3
"""Prepare page 24 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for marketing headlines and diagram labels.
Product photos, factory shots, exhibition photos and plain collages are compressed only.
Product casing text, logos, certificates and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 24

_KEEP = (
    "Keep arrows, wires, icons, colors, flags and the background. Do not move products. "
    "Do not add objects or labels that are not already in the image. Do not redesign. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, product casing text, "
    "model numbers, CE marks, display readings, button silkscreen, terminal letters N L PE, "
    "cable sizes such as 4mm² and 25mm², email addresses, or the URL www.xindun-power.com. "
    "Do not change words printed on the product such as HYBRID SOLAR INVERTER, "
    "Low Frequency Inverter, Low Frequency PV Inverter, Pure Sine Wave, "
    "SOLAR GENERATOR, ALL IN ONE SOLAR GENERATOR, or SOLAR POWER SYSTEM."
)

_IRAN_HERO = (
    "Marketing banner: inverters and batteries in front of a solar farm, Iranian flag in the headline. "
    "Translate only the white headline. "
    "'SOLAR ENERGY SYSTEM' → 'СОЛНЕЧНАЯ ЭНЕРГОСИСТЕМА'. "
    "'IN IRAN' → 'В ИРАНЕ'. "
    "Keep the Iranian flag between the lines and the two-line layout. " + _KEEP
)

_SYS3 = (
    "Wiring diagram of a blue wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Inverter' → 'Солнечный инвертор'. "
    "'Breaker' → 'Автомат' wherever it appears. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' wherever it appears. "
    "'Batteries' → 'Аккумуляторы'. "
    "'Power Grid' → 'Электросеть'. "
    "'Neutral Wire(N)' and 'Neutral Wire (N)' → 'Нейтраль (N)'. "
    "'Line Wire ( L )' and 'Line Wire (L)' → 'Фаза (L)'. "
    "'Earth Wire' → 'Заземление'. "
    "'AC Load' → 'Нагрузка AC'. "
    "Keep 4mm² and 25mm². Do not change text on the inverter screen or terminals. " + _KEEP
)

_SYS5 = (
    "Wiring diagram of a white inverter seen from the rear. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Inverter' → 'Солнечный инвертор'. "
    "'Breaker' → 'Автомат'. "
    "'Power Grid' → 'Электросеть'. "
    "'Line Wire ( L )' and 'Line Wire (L)' → 'Фаза (L)'. "
    "'Neutral Wire(N)' and 'Neutral Wire (N)' → 'Нейтраль (N)'. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' wherever it appears. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Loads' → 'Нагрузки AC'. " + _KEEP
)

_SYS10 = (
    "Wiring diagram of a black three-phase inverter cabinet. Translate only the English diagram labels. "
    "'3 Phase Inverter' → 'Трёхфазный инвертор'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч' wherever it appears. "
    "'3 Phase Load' → 'Трёхфазная нагрузка'. "
    "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
    "'Neutral Wire(N)' and 'Neutral Wire (N)' → 'Нейтраль (N)'. "
    "'Earth Wire(PE)' → 'Заземление (PE)'. "
    "'Breaker' → 'Автомат'. "
    "'Power Grid' → 'Электросеть'. "
    "Keep the single letters on the colored wires. " + _KEEP
)

_ID_BANNER = (
    "Marketing banner: Indonesian flag, solar panels, and a pale blue text panel. "
    "Translate only the black headline. "
    "'Indonesia solar exhibition 2023' → 'Выставка солнечной энергетики Индонезии 2023'. "
    "'-Xindun China' → '— Xindun, Китай'. "
    "Keep Xindun as the company name. Keep www.xindun-power.com exactly. "
    "Keep the flag, panels and logo. " + _KEEP
)

_HP = (
    "Left side is a product photo of a white inverter. Right side is a wiring diagram. "
    "Translate only the English diagram labels on the right. "
    "'Batteries' → 'Аккумуляторы'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'AC Input' → 'Вход AC'. "
    "'AC Loads' → 'Нагрузки AC'. "
    "'Power Grid or Generator' → 'Электросеть или генератор'. "
    "Keep the letters PE. Do not change HYBRID SOLAR INVERTER or text on the left product. " + _KEEP
)

_WD = (
    "Left side is a row of yellow inverters. Right side is a wiring diagram. "
    "Translate only the English diagram labels on the right. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'AC Output' → 'Выход AC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Washing Machine' → 'Стиральная машина'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'Heater' → 'Обогреватель'. "
    "'Water pump' → 'Водяной насос'. "
    "'AC Input' → 'Вход AC'. "
    "'Generator' → 'Генератор'. "
    "'Battery' → 'Аккумулятор'. "
    "Do not change text printed on the yellow units. " + _KEEP
)

_DF = (
    "Left side is a product photo. Right side is a wiring diagram of a white-and-black inverter. "
    "Translate only the English diagram labels. "
    "'PV Input' → 'Вход PV'. "
    "'AC Input' → 'Вход AC'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Lead acid/Gel/Lithium Batteries/Custom Battery' → 'Свинцовый/гелевый/литиевый/заказной аккумулятор'. "
    "'Computer/TV' → 'Компьютер/ТВ'. "
    "'Pure sine wave' → 'Чистая синусоида'. "
    "'High-power Appliances' → 'Мощные приборы'. "
    "'Household Appliances' → 'Бытовые приборы'. "
    "Do not change text printed on the product. " + _KEEP
)

_HDSX = (
    "Left side is three black cabinets. Right side is an open-cabinet wiring diagram. "
    "Translate only the English diagram labels, not silkscreen on the terminal block. "
    "'SOLAR PANELS' → 'СОЛНЕЧНЫЕ ПАНЕЛИ'. "
    "'PV COMBINER' → 'КОМБАЙНЕР PV'. "
    "'SOLAR CONTROLLER' → 'СОЛНЕЧНЫЙ КОНТРОЛЛЕР'. "
    "'BATTERIES' → 'АККУМУЛЯТОРЫ'. "
    "If a battery reads '12V200Ah Battery', translate it to 'Аккумулятор 12 В 200 А·ч'. "
    "'INVERTER' above the cabinet → 'ИНВЕРТОР'. "
    "'3-PHASE LOADS' → 'ТРЁХФАЗНЫЕ НАГРУЗКИ'. "
    "'1-PHASE LOADS' → 'ОДНОФАЗНЫЕ НАГРУЗКИ'. "
    "'POWER GRID' → 'ЭЛЕКТРОСЕТЬ'. "
    "'BREAKER' → 'АВТОМАТ'. "
    "'Earth Wire (GND)' → 'Заземление (GND)'. "
    "'A Phase' → 'Фаза A'. 'B Phase' → 'Фаза B'. 'C Phase' → 'Фаза C'. "
    "Keep the single letter N. " + _KEEP
)

_HPPLUS = (
    "Left side is a white hybrid inverter. Right side is a wiring diagram. "
    "Translate only the English diagram labels. "
    "'PV Input' → 'Вход PV'. "
    "'AC Input' → 'Вход AC'. "
    "'Generator' → 'Генератор'. "
    "'Lead Acid/Lithium Batteries' → 'Свинцовые/литиевые аккумуляторы'. "
    "'Computer/TV' → 'Компьютер/ТВ'. "
    "'Pure sine wave' → 'Чистая синусоида'. "
    "'High-power Appliances' → 'Мощные приборы'. "
    "'Household Appliances' → 'Бытовые приборы'. "
    "The line on the inverter must stay 'HYBRID SOLAR INVERTER'. " + _KEEP
)

_ZW_POTENTIAL = (
    "Marketing banner: a white inverter over a solar farm and a teal headline panel. "
    "Translate only the white headline. "
    "'Potential of Inverters in Zimbabwe market' → 'Потенциал рынка инверторов в Зимбабве'. "
    "Keep sales@gdxindun.com and www.xindun-power.com exactly. "
    "Do not change text on the inverter. " + _KEEP
)

_ZW_HARARE = (
    "Marketing banner: a blue inverter beside solar panels, with a white caption bar. "
    "Translate only the caption. "
    "'SOLAR INVERTERS HARARE' → 'СОЛНЕЧНЫЕ ИНВЕРТОРЫ ХАРАРЕ'. "
    "'THE KEY TO GREEN ENERGY' → 'КЛЮЧ К ЗЕЛЁНОЙ ЭНЕРГИИ'. "
    "Do not change 'SOLAR POWER SYSTEM' printed on the blue unit. " + _KEEP
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "iran_hero": "https://www.xindun-power.com/uploadfile/2024/09/23/20240923134000x2on8b.jpg",
    "sys3": "https://www.xindun-power.com/uploadfile/2024/09/20/20240920170854eDKuwL.jpg",
    "sys5": "https://www.xindun-power.com/uploadfile/2024/09/20/20240920170909Q1oBd4.jpg",
    "sys10": "https://www.xindun-power.com/uploadfile/2024/09/20/20240920170924akwYo8.jpg",
    "price_hero": "https://www.xindun-power.com/uploadfile/2024/08/29/20240829150413YXPBvc.jpg",
    "price_kit": "https://www.xindun-power.com/uploadfile/2024/08/29/20240829150639imZUzk.jpg",
    "id_banner": "https://www.xindun-power.com/uploadfile/2023/03/17/202303171715527122.jpg",
    "id_booth": "https://www.xindun-power.com/uploadfile/2023/04/10/202304100915559642.jpg",
    "id_collage": "https://www.xindun-power.com/uploadfile/2023/04/10/202304100917018926.jpg",
    "zm_hero": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202151316xiRTye.jpg",
    "zm_line": "https://www.xindun-power.com/uploadfile/2023/12/02/2023120215142430cgwq.jpg",
    "zm_hp": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202164937qnu2rI.jpg",
    "zm_wd": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202164938A4bCkT.jpg",
    "zm_df": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202164939pR4ML8.jpg",
    "zm_hdsx": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202164939AjhOGq.jpg",
    "zm_plus": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202164940s6iOYL.jpg",
    "zm_room": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202151510faU7Rm.jpg",
    "zm_lab": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202151542IABJlj.jpg",
    "zw_hero": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021356579LSlRW.jpg",
    "zw_potential": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202135749TDstRf.jpg",
    "zw_line": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021359352HBb84.jpg",
    "zw_harare": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202140115jbaTZ9.jpg",
    "zw_hp": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202142114rU9wHt.jpg",
    "zw_plus": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202142124lnKJGg.jpg",
    "zw_lf": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202142132OL5ku6.jpg",
    "zw_df": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202142141zJB1th.jpg",
    "zw_ess": "https://www.xindun-power.com/uploadfile/2023/12/02/2023120214215289H4eC.jpg",
    "zw_factory": "https://www.xindun-power.com/uploadfile/2023/12/02/20231202140340i1gVGs.jpg",
    "zw_show": "https://www.xindun-power.com/uploadfile/2023/12/02/202312021403545H3O6B.jpg",
}

DUOMI_BY_URL = {
    U["iran_hero"]: _IRAN_HERO,
    U["sys3"]: _SYS3,
    U["sys5"]: _SYS5,
    U["sys10"]: _SYS10,
    U["id_banner"]: _ID_BANNER,
    U["zm_hp"]: _HP,
    U["zm_wd"]: _WD,
    U["zm_df"]: _DF,
    U["zm_hdsx"]: _HDSX,
    U["zm_plus"]: _HPPLUS,
    U["zw_potential"]: _ZW_POTENTIAL,
    U["zw_harare"]: _ZW_HARARE,
}

IMAGE_SOURCES = [
    [
        _im(U["iran_hero"], "Солнечная энергосистема в Иране"),
        _im(U["sys3"], "Солнечная энергосистема 3 кВт хит продаж в Иране"),
        _im(U["sys5"], "Солнечная энергосистема 5 кВт хит продаж в Иране"),
        _im(U["sys10"], "Солнечная энергосистема 10 кВт хит продаж в Иране"),
    ],
    [
        _im(U["price_hero"], "Цена солнечной панели с инвертором и аккумулятором"),
        _im(U["price_kit"], "Цена комплекта солнечной системы на 10 кВт с панелью инвертором и аккумулятором"),
    ],
    [
        _im(U["id_booth"], "Стенд Xindun на выставке солнечной энергетики Индонезии 2023"),
        _im(U["id_banner"], "Выставка солнечной энергетики Индонезии 2023 Xindun Китай"),
        _im(U["id_collage"], "Павильон Китая на выставке солнечной энергетики Индонезии 2023"),
    ],
    [
        _im(U["zm_hero"], "Солнечный инвертор в Замбии"),
        _im(U["zm_line"], "Инверторы в продаже в Замбии"),
        _im(U["zm_hp"], "Инвертор HP PRO-T в продаже в Замбии"),
        _im(U["zm_wd"], "Инвертор WD в продаже в Замбии"),
        _im(U["zm_df"], "Инвертор DF в продаже в Замбии"),
        _im(U["zm_hdsx"], "Трёхфазный инвертор HDSX в продаже в Замбии"),
        _im(U["zm_plus"], "Инвертор HP PLUS плюс в продаже в Замбии"),
        _im(U["zm_room"], "Шоурум инверторов для Замбии"),
        _im(U["zm_lab"], "Испытания солнечного инвертора для Замбии"),
    ],
    [
        _im(U["zw_hero"], "Солнечные инверторы в продаже в Зимбабве"),
        _im(U["zw_potential"], "Потенциал рынка инверторов в Зимбабве"),
        _im(U["zw_line"], "Линейка солнечных инверторов для Зимбабве"),
        _im(U["zw_harare"], "Солнечные инверторы в Хараре ключ к зелёной энергии"),
        _im(U["zw_hp"], "Инвертор 5 кВА HP PRO-T для Зимбабве"),
        _im(U["zw_plus"], "Инвертор 5 кВА HP PLUS для Зимбабве"),
        _im(U["zw_lf"], "Инвертор 5 кВА LF для Зимбабве"),
        _im(U["zw_df"], "Инвертор 5 кВА DF для Зимбабве"),
        _im(U["zw_ess"], "Солнечный генератор ESS 5 кВА для Зимбабве"),
        _im(U["zw_factory"], "Завод солнечных инверторов для продажи в Хараре"),
        _im(U["zw_show"], "Инверторы Xindun на выставке для продажи в Хараре"),
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
