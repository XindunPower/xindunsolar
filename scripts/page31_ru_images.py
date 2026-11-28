#!/usr/bin/env python3
"""Prepare page 31 Russian images.

Listing heroes are index 0 and become featured_media only.
Duomi gpt-image-2 only for English marketing headlines, product-card captions
and wiring-diagram labels. Factory floors, certificates, installation photos
and plain product shots are compressed only. Product casing text, logos,
port silkscreen and wall company names stay unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import page21_ru_images as engine  # noqa: E402

PAGE_NUM = 31

_KEEP = (
    "Keep arrows, icons, colors, people, products and the background. "
    "Do not move products or people. Do not add objects or labels that are not already in the image. "
    "Do not redesign the poster. "
    "Do NOT change the xindun logo, Xindun GREEN POWER, GREENPOWER, "
    "product casing text, model numbers, display readings, port silkscreen, CE marks, "
    "Chinese characters, certificates, exhibition booth signs, or the URL www.xindun-power.com. "
    "Do not change words printed on the product such as ALL IN ONE SOLAR GENERATOR, "
    "SOLAR GENERATOR, HYBRID SOLAR INVERTER, PURE SINE WAVE INVERTER, SOLAR POWER SYSTEM, "
    "or SOLAR POWER INVERTER."
)


def _im(src: str, alt: str) -> dict:
    return {"src": src, "alt_ru": alt, "title_ru": alt}


U = {
    "mppt_hero": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031532427112.jpg",
    "mppt_nobatt": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031534022028.jpg",
    "mains_cur": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031534523178.jpg",
    "hpt_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031535554192.jpg",
    "hpt_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031536142680.jpg",
    "hp_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031537393320.jpg",
    "hp_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031538105222.jpg",
    "ls_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031538551338.jpg",
    "ls_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031539161266.jpg",
    "dp_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031540377111.jpg",
    "dp_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031540555074.jpg",
    "mfr_off": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031542354449.jpg",
    "mfr_app": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031543071557.jpg",
    "pp_hero": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031151354439.jpg",
    "gpc_line": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031419001752.jpg",
    "gpc_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031419437480.jpg",
    "gpc_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031420069630.jpg",
    "dp2_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031421135640.jpg",
    "dp2_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031421343400.jpg",
    "da_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031422394439.jpg",
    "da_w": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031423013770.jpg",
    "ess_p": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031424025429.jpg",
    "ess_w1": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031424241914.jpg",
    "ess_w2": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031424482442.jpg",
    "pp_app": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031426332462.jpg",
    "pp_fac": "https://www.xindun-power.com/uploadfile/2023/07/03/202307031427315479.jpg",
    "eff_hero": "https://www.xindun-power.com/uploadfile/2023/06/21/202306210959554588.jpg",
    "eff_how": "https://www.xindun-power.com/uploadfile/2023/06/21/202306211000289899.jpg",
    "eff_v": "https://www.xindun-power.com/uploadfile/2023/06/21/202306211000581722.jpg",
    "eff_fac": "https://www.xindun-power.com/uploadfile/2023/06/21/202306211002027249.jpg",
    "eff_cus": "https://www.xindun-power.com/uploadfile/2023/06/21/202306211002228724.jpg",
    "cn_hero": "https://www.xindun-power.com/uploadfile/2023/06/14/202306141533206457.jpg",
    "cn_bldg": "https://www.xindun-power.com/uploadfile/2023/06/14/202306141533546585.jpg",
    "cn_fac": "https://www.xindun-power.com/uploadfile/2023/06/14/202306141534269715.jpg",
    "cn_cert": "https://www.xindun-power.com/uploadfile/2023/06/14/202306141540032099.jpg",
    "cn_line": "https://www.xindun-power.com/uploadfile/2023/06/14/202306141625335263.jpg",
    "vn_hero": "https://www.xindun-power.com/uploadfile/2023/06/13/202306131200132888.jpg",
    "vn_hyb": "https://www.xindun-power.com/uploadfile/2023/06/12/202306121131265267.jpg",
    "vn_inst": "https://www.xindun-power.com/uploadfile/2023/06/12/202306121135072675.jpg",
    "vn_fac": "https://www.xindun-power.com/uploadfile/2023/06/12/202306121133453834.jpg",
    "vn_ess": "https://www.xindun-power.com/uploadfile/2023/06/13/202306131611256337.jpg",
    "vn_inv": "https://www.xindun-power.com/uploadfile/2023/06/14/202306140857527851.jpg",
}

_MPPT_HERO = (
    "A marketing banner: three inverters in a flower field under solar panels, with a white text card on a green panel. "
    "Translate only the three green lines inside the white card. Keep three lines. "
    "Line 1 'Inverter with' → 'Инвертор с'. "
    "Line 2 'solar mppt &' → 'солнечным MPPT и'. "
    "Line 3 'mains charger' → 'зарядом от сети'. "
    "Keep the logo and the URL www.xindun-power.com. Keep MPPT in Latin letters. " + _KEEP
)

_NOBATT = (
    "A product graphic of a white hybrid inverter, a circuit-board callout and a crossed-out battery. "
    "Translate only the blue headline and the callout caption. Keep two headline lines. "
    "Line 1 'Built-In MPPT Can Be Used' → 'Встроенный MPPT работает'. "
    "Line 2 'Without Battery' → 'без аккумулятора'. "
    "Callout 'Built-in MPPT' → 'Встроенный MPPT'. "
    "Keep MPPT in Latin letters. "
    "Do NOT change HYBRID SOLAR INVERTER, the display or the logo on the unit. " + _KEEP
)

_MAINS = (
    "A product graphic of a white hybrid inverter with a large pale 60A watermark. "
    "Translate only the blue title and the three black lines under it. Keep the title on one line and the body on three lines. "
    "Title 'Mains charging current' → 'Ток заряда от сети'. "
    "Line 1 'The mains charging current is very large and can reach 60A,' → 'Ток заряда от сети очень большой и доходит до 60 А,'. "
    "Line 2 'Far more than the 30A maximum current of' → 'это намного больше максимума 30 А'. "
    "Line 3 'the low frequency inverter' → 'у низкочастотного инвертора'. "
    "Keep 60A and 30A numerals. "
    "Do NOT change HYBRID SOLAR INVERTER, the display or the logo on the unit. " + _KEEP
)

_HP_WIRE = (
    "A wiring diagram of a white hybrid inverter. Translate only the English diagram labels. "
    "'Power Grid' → 'Электросеть'. "
    "'OR' → 'ИЛИ'. "
    "'Generator' → 'Генератор'. "
    "'AC INPUT' → 'ВХОД AC'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Battery' → 'Аккумулятор'. "
    "'AC OUTPUT' → 'ВЫХОД AC'. "
    "'Refrigerator' → 'Холодильник'. "
    "'Air conditioner' → 'Кондиционер'. "
    "'Washing machine' → 'Стиральная машина'. "
    "'TV' → 'ТВ'. "
    "'Rice cooker' → 'Рисоварка'. "
    "Keep AC in Latin letters. "
    "Do NOT change HYBRID SOLAR INVERTER printed on the unit. " + _KEEP
)

_HP_REAR = (
    "A rear-view wiring diagram of a white-and-black inverter. Translate only the callout labels beside the drawing. "
    "Do NOT change port silkscreen on the black panel: BATTERY, AC INPUT, AC OUTPUT, SOLAR, ATTENTION or the PE marks printed on the chassis. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Input' → 'Вход AC'. "
    "'Solar Panels' → 'Солнечные панели'. "
    "Both 'AC Loads' labels → 'Нагрузка AC'. "
    "'Power Grid' → 'Электросеть'. "
    "The small word 'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "Keep N, L, PE and AC in Latin letters. "
    "Do NOT change text printed on the two batteries. " + _KEEP
)

_LS_WIRE = (
    "A wiring diagram of a blue wall inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'DC Loads' → 'Нагрузка DC'. "
    "'AC Input' → 'Вход AC'. "
    "'AC Output' → 'Выход AC'. "
    "'Battery' → 'Аккумулятор'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "Keep N, L, PE, AC and DC in Latin letters. "
    "Do NOT change SOLAR POWER SYSTEM printed on the unit or the text printed on the battery. " + _KEEP
)

_DP_WIRE = (
    "A wiring diagram of a silver low-frequency inverter. Translate only the English diagram labels. "
    "The misspelled label 'SoarI Panels' → 'Солнечные панели'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'DC Loads' → 'Нагрузка DC'. "
    "'Neutral Wire' → 'Нейтраль' in both places. "
    "'Live Wire' → 'Фаза' in both places. "
    "'Ground Wire' → 'Заземление'. "
    "'Power Grid or Generator' → 'Сеть или генератор'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'Loads for each AC output socket should not exceed 1KW' → 'Нагрузка каждой розетки AC не более 1 кВт'. "
    "Keep DC, AC and 1KW numerals readable. "
    "Do NOT change PURE SINE WAVE INVERTER or other text printed on the unit. " + _KEEP
)

_APP_COLLAGE = (
    "A six-photo installation collage. Translate only the English label 'PV combiner box' → 'Бокс объединения PV'. "
    "Do NOT change the Chinese warning characters, the logo, or any text printed on the inverters and batteries. "
    "Keep PV in Latin letters. " + _KEEP
)

_PP_HERO = (
    "A marketing banner of several inverters on a white and green background. "
    "Translate only the left-side headline. Keep the green title, the rule and the question on three lines. "
    "'Plug n Play' → 'Подключи и работай'. "
    "Line 'What is a' → 'Что такое'. "
    "Line 'plug and play inverter?' → 'инвертор «подключи и работай»?'. "
    "Keep the question mark, the logo and the green URL badge www.xindun-power.com. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or SOLAR GENERATOR printed on the cabinets. " + _KEEP
)

_GPC_SOCK = (
    "Four portable inverters in a row and a round close-up of a socket. "
    "Translate only the caption under the close-up. Keep two lines. "
    "'AC 220V' → 'AC 220 В'. "
    "'MULTI-FUNCTION SOCKET' → 'УНИВЕРСАЛЬНАЯ РОЗЕТКА'. "
    "Also translate the same 'AC 220V' printed inside the round inset → 'AC 220 В'. "
    "Keep AC in Latin letters. "
    "Do NOT change model text, VOLTAGE OUTPUT, BATTERY VOLTAGE or other silkscreen on the inverters. " + _KEEP
)

_GPC_WIRE = (
    "A compact wiring diagram of two blue inverters, panels, a controller and a battery. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Solar Input' → 'Вход солнца'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'AC Output' → 'Выход AC'. "
    "'Battery' → 'Аккумулятор'. "
    "Keep AC in Latin letters. "
    "Do NOT change text printed on the blue inverters or on the battery. " + _KEEP
)

_DP2_WIRE = (
    "A block wiring diagram: panels, a tower, a generator, an orange controller, a battery and a white inverter. "
    "Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Power Grid' → 'Электросеть'. "
    "'or' → 'или'. "
    "'Generator' → 'Генератор'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "Keep AC in Latin letters. "
    "Do NOT change text printed on the white inverter or on the battery. " + _KEEP
)

_DA_WIRE = (
    "A block wiring diagram of a blue inverter. Translate only the English diagram labels. "
    "'Solar Panels' → 'Солнечные панели'. "
    "'Power Grid' → 'Электросеть'. "
    "'Generator' → 'Генератор'. "
    "'or' → 'или'. "
    "'Solar Controller' → 'Солнечный контроллер'. "
    "'Batteries' → 'Аккумуляторы'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "Keep AC in Latin letters. Do NOT change text printed on the blue inverter. " + _KEEP
)

_ESS_W1 = (
    "A wiring diagram of two wheeled solar-generator cabinets. Translate only the English diagram labels. "
    "Keep the misspelled source wording as the string to find, but write correct Russian. "
    "'4pcs 330W solar panel connect in parallel' → '4 панели 330 Вт параллельно'. "
    "'Spare Battery' → 'Запасной аккумулятор'. "
    "Each 'Live Wire(L)' → 'Фаза (L)'. "
    "Each 'Neutral Wire(N)' → 'Нейтраль (N)'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'Power Grid' → 'Электросеть'. "
    "'Or' → 'Или'. "
    "'Diesel generators' → 'Дизельные генераторы'. "
    "'Breaker' → 'Автомат'. "
    "The title 'Solar Generrtor: Built-in 3KW 24V inverter +24V 60A MPPT+2pcs 12V 200Ah Gel battery' → "
    "'Солнечный генератор: встроенный инвертор 3 кВт 24 В + MPPT 24 В 60 А + 2 гелевых аккумулятора 12 В 200 А·ч'. "
    "'USB 5V Loads (DC 5V Output)' → 'Нагрузка USB 5 В (выход DC 5 В)'. "
    "'DC Loads (DC 12V Output)' → 'Нагрузка DC (выход DC 12 В)'. "
    "'Battery positive (connected to the red wire)' → 'Плюс аккумулятора (красный провод)'. "
    "'Battery negative (connected to the black wire)' → 'Минус аккумулятора (чёрный провод)'. "
    "Each '12V200Ah Battery' → 'Аккумулятор 12 В 200 А·ч'. "
    "Keep L, N, AC, DC, USB, MPPT and the numerals. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or other text printed on the cabinets. " + _KEEP
)

_ESS_W2 = (
    "A wiring diagram of one wheeled solar generator, shown closed and open. Translate only the English diagram labels. "
    "'2pcs 160W solar panel connect in parallel' → '2 панели 160 Вт параллельно'. "
    "'Diesel generators' → 'Дизельные генераторы'. "
    "'Or' → 'Или'. "
    "'Power Grid' → 'Электросеть'. "
    "'Breaker' → 'Автомат'. "
    "Each 'Live Wire(L)' → 'Фаза (L)'. "
    "Each 'Neutral Wire(N)' → 'Нейтраль (N)'. "
    "The title 'Solar Generrtor: Built-in 1000W 12V inverter +12V 40A PWM+1pc 12V 100Ah Gel battery' → "
    "'Солнечный генератор: встроенный инвертор 1000 Вт 12 В + PWM 12 В 40 А + 1 гелевый аккумулятор 12 В 100 А·ч'. "
    "'USB 5V Loads (DC 5V Output)' → 'Нагрузка USB 5 В (выход DC 5 В)'. "
    "'DC Loads (DC 12V Output)' → 'Нагрузка DC (выход DC 12 В)'. "
    "'AC Loads' → 'Нагрузка AC'. "
    "'Battery negative (connected to the black wire)' → 'Минус аккумулятора (чёрный провод)'. "
    "'Battery positive (connected to the red wire)' → 'Плюс аккумулятора (красный провод)'. "
    "'12V100Ah Battery' → 'Аккумулятор 12 В 100 А·ч'. "
    "Keep L, N, AC, DC, USB, PWM and the numerals. "
    "Do NOT change SOLAR GENERATOR printed on the cabinet. " + _KEEP
)

_PP_APP = (
    "A green collage of six lifestyle photos under one headline. Translate only the headline and the six white captions. "
    "'Application of plug n play inverters' → 'Где применяют инверторы «подключи и работай»'. "
    "'home' → 'дом'. "
    "'camping' → 'кемпинг'. "
    "'RV' → 'автодом'. "
    "'ship' → 'судно'. "
    "'car' → 'автомобиль'. "
    "'office' → 'офис'. "
    "Keep the logo. " + _KEEP
)

_EFF_HERO = (
    "A marketing banner of four inverters in front of solar panels. "
    "Translate only the white line and the green badge. Keep two lines. "
    "'What Is The Most Efficient' → 'Какой самый эффективный'. "
    "'SOLAR POWER INVERTER' → 'СОЛНЕЧНЫЙ ИНВЕРТОР'. "
    "Keep the logo. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or SOLAR GENERATOR printed on the units. " + _KEEP
)

_EFF_HOW = (
    "A flat illustration of a house, a sun and one wall inverter inside a dotted circle. "
    "Translate only the white question. Keep two lines and the question mark. "
    "Line 1 'How can I improve' → 'Как повысить'. "
    "Line 2 'my inverter efficiency?' → 'КПД моего инвертора?'. "
    "Keep the logo. Do NOT change text printed on the small inverter. " + _KEEP
)

_EFF_V = (
    "Two all-in-one cabinets on a garden patio, with a blue banner and two voltage badges. "
    "Translate only the banner sentence. Keep one line and the question mark. "
    "'Which is the most efficient solar inverter 24V or 48V ?' → "
    "'Какой солнечный инвертор эффективнее: 24 В или 48 В?'. "
    "Keep the badges '48V' and '24V' as '48 В' and '24 В'. "
    "Keep the logo. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR printed on the cabinets. " + _KEEP
)

_CN_HERO = (
    "A factory photo with a green curved overlay and a white headline. "
    "Translate only the white headline. Keep three lines and the question mark. "
    "Line 1 'How do I find' → 'Как найти'. "
    "Line 2 'Solar Inverter' → 'производителей солнечных'. "
    "Line 3 'Manufacturers in China?' → 'инверторов в Китае?'. "
    "The full question must read 'Как найти производителей солнечных инверторов в Китае?'. "
    "Keep the logo and the URL www.xindun-power.com. "
    "Do NOT change Chinese signs in the factory. " + _KEEP
)

_VN_HERO = (
    "A sunset landscape of mountains and solar panels with a green band and the Vietnam flag. "
    "Translate only the two white lines. Keep the flag, the logo and the URL www.xindun-power.com. "
    "Line 1 'Solar energy photovoltaic system' → 'Солнечная фотоэлектрическая система'. "
    "Line 2 'for vietnam power shortage' → 'при нехватке энергии во Вьетнаме'. " + _KEEP
)

_VN_HYB = (
    "A house diagram with rooftop panels, a yellow cabinet, appliances and a power line. "
    "Translate only the three English labels. "
    "Title 'Hybrid solar energy photovoltaic system' → 'Гибридная солнечная фотоэлектрическая система'. "
    "'off grid inverter' → 'автономный инвертор' on two lines if needed. "
    "'battery bank' → 'блок аккумуляторов'. "
    "Keep the logo. Do NOT change text printed on the yellow cabinet. " + _KEEP
)

_VN_ESS = (
    "Two product cards side by side, each a solar array and a cabinet, with a caption under each card. "
    "Translate only the two captions. Do not change the photographs or the two-card layout. "
    "'ESS solar generator 1500-7000W' → 'Солнечный генератор ESS 1500–7000 Вт'. "
    "'ESS solar generator 300-1000W' → 'Солнечный генератор ESS 300–1000 Вт'. "
    "Keep ESS in Latin letters and the power numbers. "
    "Do NOT change ALL IN ONE SOLAR GENERATOR or SOLAR GENERATOR printed on the cabinets. " + _KEEP
)

_VN_INV = (
    "Two product cards side by side, each a solar array and inverters, with a caption under each card. "
    "Translate only the two captions. Do not change the photographs or the two-card layout. "
    "'HP PRO-T hybrid solar inverter 1KW-8KW' → 'Гибридный солнечный инвертор HP PRO-T 1–8 кВт'. "
    "'LS solar inverter 1KW-6KW' → 'Солнечный инвертор LS 1–6 кВт'. "
    "Keep HP PRO-T and LS in Latin letters. "
    "Do NOT change text printed on the inverters. " + _KEEP
)

DUOMI_BY_URL = {
    U["mppt_hero"]: _MPPT_HERO,
    U["mppt_nobatt"]: _NOBATT,
    U["mains_cur"]: _MAINS,
    U["hpt_w"]: _HP_WIRE,
    U["hp_w"]: _HP_REAR,
    U["ls_w"]: _LS_WIRE,
    U["dp_w"]: _DP_WIRE,
    U["mfr_app"]: _APP_COLLAGE,
    U["pp_hero"]: _PP_HERO,
    U["gpc_line"]: _GPC_SOCK,
    U["gpc_w"]: _GPC_WIRE,
    U["dp2_w"]: _DP2_WIRE,
    U["da_w"]: _DA_WIRE,
    U["ess_w1"]: _ESS_W1,
    U["ess_w2"]: _ESS_W2,
    U["pp_app"]: _PP_APP,
    U["eff_hero"]: _EFF_HERO,
    U["eff_how"]: _EFF_HOW,
    U["eff_v"]: _EFF_V,
    U["cn_hero"]: _CN_HERO,
    U["vn_hero"]: _VN_HERO,
    U["vn_hyb"]: _VN_HYB,
    U["vn_ess"]: _VN_ESS,
    U["vn_inv"]: _VN_INV,
}

IMAGE_SOURCES = [
    [
        _im(U["mppt_hero"], "Инвертор с солнечным MPPT и зарядным устройством от сети"),
        _im(U["mppt_nobatt"], "Инвертор с солнечным MPPT без аккумулятора"),
        _im(U["mains_cur"], "Инвертор с зарядным устройством от сети"),
        _im(U["hpt_p"], "Инвертор HP PRO-T с солнечным MPPT и зарядом от сети"),
        _im(U["hpt_w"], "Схема подключения инвертора HP PRO-T с солнечным MPPT и зарядом от сети"),
        _im(U["hp_p"], "Инвертор HP PRO с солнечным MPPT и зарядом от сети"),
        _im(U["hp_w"], "Схема подключения инвертора HP PRO с солнечным MPPT и зарядом от сети"),
        _im(U["ls_p"], "Инвертор LS с солнечным MPPT и зарядом от сети"),
        _im(U["ls_w"], "Схема подключения инвертора LS с солнечным MPPT и зарядом от сети"),
        _im(U["dp_p"], "Инвертор DP с солнечным MPPT и зарядом от сети"),
        _im(U["dp_w"], "Схема подключения инвертора DP с солнечным MPPT и зарядом от сети"),
        _im(U["mfr_off"], "Производитель инверторов с солнечным MPPT и зарядом от сети"),
        _im(U["mfr_app"], "Применение инвертора с солнечным MPPT и зарядом от сети"),
    ],
    [
        _im(U["pp_hero"], "Инверторы «подключи и работай» изменили нашу жизнь"),
        _im(U["gpc_line"], "Инвертор GP-C «подключи и работай» в продаже"),
        _im(U["gpc_p"], "Инвертор GP-C «подключи и работай»"),
        _im(U["gpc_w"], "Схема подключения инвертора GP-C «подключи и работай»"),
        _im(U["dp2_p"], "Солнечный инвертор DP «подключи и работай»"),
        _im(U["dp2_w"], "Схема подключения солнечного инвертора DP «подключи и работай»"),
        _im(U["da_p"], "Инвертор DA «подключи и работай» в продаже"),
        _im(U["da_w"], "Схема подключения инвертора DA «подключи и работай»"),
        _im(U["ess_p"], "Инвертор ESS «подключи и работай» с аккумуляторами"),
        _im(U["ess_w1"], "Схема подключения инвертора ESS «подключи и работай» на 3 кВт"),
        _im(U["ess_w2"], "Схема подключения инвертора ESS «подключи и работай» на 1000 Вт"),
        _im(U["pp_app"], "Применение инверторов «подключи и работай»"),
        _im(U["pp_fac"], "Производитель инверторов «подключи и работай»"),
    ],
    [
        _im(U["eff_hero"], "Какой самый эффективный силовой и солнечный инвертор"),
        _im(U["eff_how"], "Как повысить КПД инвертора"),
        _im(U["eff_v"], "Какой солнечный инвертор эффективнее, 24 В или 48 В"),
        _im(U["eff_fac"], "Производитель самых эффективных силовых и солнечных инверторов"),
        _im(U["eff_cus"], "Заказчики инверторов Xindun по всему миру"),
    ],
    [
        _im(U["cn_hero"], "Как найти производителей солнечных инверторов в Китае"),
        _im(U["cn_bldg"], "Xindun Power, производитель солнечных инверторов в Китае"),
        _im(U["cn_fac"], "Завод Xindun Power, производитель солнечных инверторов в Китае"),
        _im(U["cn_cert"], "Сертификаты Xindun Power, производитель солнечных инверторов в Китае"),
        _im(U["cn_line"], "Солнечный инвертор Xindun Power"),
    ],
    [
        _im(U["vn_hero"], "Солнечная фотоэлектрическая система при нехватке энергии во Вьетнаме"),
        _im(U["vn_hyb"], "Гибридная солнечная фотоэлектрическая система"),
        _im(U["vn_inst"], "Применение солнечной фотоэлектрической системы"),
        _im(U["vn_fac"], "Производитель солнечных фотоэлектрических систем Xindun"),
        _im(U["vn_ess"], "Солнечная фотоэлектрическая система Xindun"),
        _im(U["vn_inv"], "Солнечная энергетическая фотоэлектрическая система Xindun"),
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
