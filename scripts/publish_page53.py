#!/usr/bin/env python3
"""Publish xindun-power news page 53 articles to Spanish WordPress (cat 89)."""

from __future__ import annotations

import json
import importlib.util
import subprocess
import time
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
BASE_PATH = REPO / "scripts" / "publish_page52.py"


def load_base():
    spec = importlib.util.spec_from_file_location("publish_page52_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load base module: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    base = load_base()

    def run_duomi_relaxed(
        image_url: str,
        extra_prompt: str,
        name: str,
        size: str,
        orig_wh: tuple[int, int],
        orig_path: Path,
        attempts: int = 4,
    ) -> Path | None:
        prompt = f"{base.PROMPT_BASE} {extra_prompt}"
        final = base.OUT / f"{name}.webp"
        for attempt in range(attempts):
            out_name = f"{name}-try{attempt}"
            print(f"[duomi] {name} attempt={attempt + 1} size={size}", flush=True)
            cmd = [
                "python3",
                str(REPO / "scripts" / "duomi_image.py"),
                "--image-url",
                image_url,
                "--prompt",
                prompt,
                "--size",
                size,
                "--output-name",
                out_name,
                "--max-kb",
                "0",
                "--print-json",
                "--timeout",
                "600",
            ]
            p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
            files: list[str] = []
            for line in (p.stdout or "").splitlines()[::-1]:
                line = line.strip()
                if line.startswith("{"):
                    try:
                        files = json.loads(line).get("files") or []
                        break
                    except Exception:  # noqa: BLE001
                        pass
                if line.startswith("SUCCESS:"):
                    files = [line.split("SUCCESS:", 1)[1].strip()]
                    break
            if not files:
                print(f"[duomi] no files stderr={(p.stderr or '')[-400:]}", flush=True)
                time.sleep(5)
                continue

            raw = Path(files[0])
            if not raw.exists():
                print(f"[duomi] output missing: {raw}", flush=True)
                time.sleep(3)
                continue

            try:
                with base.Image.open(raw) as chk:
                    cw, ch = chk.size
                ratio_delta = abs((cw / ch) - (orig_wh[0] / orig_wh[1]))
                # This page has one 1.625:1 source image while Duomi emits fixed buckets;
                # keep a moderate ratio tolerance but still hard-reject true layout drift.
                if ratio_delta > 0.18:
                    print(f"[duomi] reject ratio {cw}x{ch} vs {orig_wh}", flush=True)
                    time.sleep(3)
                    continue
                diff_score = base.image_mean_diff(orig_path, raw, orig_wh[0], orig_wh[1])
                if diff_score > 45.0:
                    print(f"[duomi] reject redesign diff={diff_score:.2f}", flush=True)
                    time.sleep(3)
                    continue
                base.encode_webp(raw, final, orig_wh[0], orig_wh[1], 100)
            except Exception as exc:  # noqa: BLE001
                print(f"[duomi] layout/compress failed: {exc}", flush=True)
                time.sleep(3)
                continue
            if final.exists() and final.stat().st_size > 0:
                return final
        return None

    base.run_duomi = run_duomi_relaxed

    base.PAGE_NUM = 53
    base.NEWS_URL = f"https://www.xindun-power.com/news/{base.PAGE_NUM}.html"
    base.RESULTS_PATH = Path("/tmp/page53_results.json")

    # Only images with English marketing/diagram overlays use Duomi.
    # The rest are real photos/product shots and are kept unchanged except compression.
    base.DUOMI_MAP = {
        (1, 0): (
            "Translate the bottom marketing strip text only to Spanish: "
            "'Pure sine wave inverter'→'Inversor de onda sinusoidal pura'; "
            "'Solar charge controller'→'Controlador de carga solar'. "
            "Keep Chinese text, product lineup, background, and all logos unchanged. "
            "Do not redesign."
        ),
        (2, 1): (
            "Translate diagram labels only to Spanish: "
            "'AC output switch'→'Interruptor de salida CA'; "
            "'AC input switch'→'Interruptor de entrada CA'; "
            "'Battery switch'→'Interruptor de batería'; "
            "'Battery'→'Batería'; "
            "'Grid or generator'→'Red o generador'; "
            "'Three-phase load'→'Carga trifásica'. "
            "Keep wiring colors, symbols, product casing text, and layout unchanged."
        ),
        (3, 0): (
            "Translate feature callout text only to Spanish: "
            "'LCD integration display'→'Pantalla LCD integrada'; "
            "'Smooth metal fuselage, can print your logo'→"
            "'Carcasa metálica lisa, se puede imprimir su logotipo'; "
            "'Cooling fan in intelligent control'→'Ventilador de enfriamiento con control inteligente'; "
            "'UPS / INV Dial switch'→'Selector giratorio UPS / INV'; "
            "'Optional'→'Opcional'. "
            "Keep RS485/RS232 labels, product logos, and all hardware details unchanged."
        ),
        (3, 1): (
            "Translate PCB feature text only to Spanish: "
            "'Industrial circuit motherboard'→'Placa principal de circuito industrial'; "
            "'fine workmanship, full solder joints, stable'→"
            "'acabado fino, soldaduras completas, estable'; "
            "'Built-in solar controller'→'Controlador solar integrado'; "
            "'Save space, reduce packing costs, make wiring more convenient'→"
            "'Ahorra espacio, reduce costos de embalaje y hace el cableado más conveniente'; "
            "'High frequency copper wire transformer'→'Transformador de alambre de cobre de alta frecuencia'; "
            "'Light weight, large load current, good impact resistance, stable, high efficiency'→"
            "'Peso ligero, gran corriente de carga, buena resistencia al impacto, estable, alta eficiencia'. "
            "Keep product internals and circle callout graphics unchanged."
        ),
        (3, 2): (
            "Translate wiring diagram labels only to Spanish: "
            "'Solar Panels 1'→'Paneles solares 1'; "
            "'Solar Panels 2'→'Paneles solares 2'; "
            "'Batteries'→'Baterías'; "
            "'AC Input'→'Entrada CA'; "
            "'AC Output'→'Salida CA'; "
            "'Power Grid'→'Red eléctrica'; "
            "'Generator'→'Generador'; "
            "'or'→'o'; "
            "'AC Loads'→'Cargas CA'. "
            "Keep PE/N/L markings, wiring lines, and product details unchanged."
        ),
        (3, 4): (
            "Translate system diagram labels only to Spanish: "
            "'Solar Panels'→'Paneles solares'; "
            "'Off-Grid Hybrid Solar Inverter (Can work withou battery)'→"
            "'Inversor solar híbrido aislado (puede funcionar sin batería)'; "
            "'Generator'→'Generador'; "
            "'Power Grid'→'Red eléctrica'; "
            "'Batteries (Optional)'→'Baterías (Opcional)'; "
            "'AC Loads'→'Cargas CA'; "
            "'or'→'o'. "
            "Keep dashed wiring layout, product photos, and symbols unchanged."
        ),
        (3, 5): (
            "Translate marketing panel text only to Spanish: "
            "'Customizable - OEM - Factory Wholesale'→'Personalizable - OEM - Venta al por mayor de fábrica'; "
            "'Emergency Backup Power'→'Energía de respaldo de emergencia'; "
            "'Hilltop / Island / Boat'→'Cima / Isla / Barco'; "
            "'Photovoltaic RV'→'Autocaravana fotovoltaica'; "
            "'Daily Home Appliances'→'Electrodomésticos diarios'. "
            "Keep product images, arrows, green bars, and overall poster layout unchanged."
        ),
    }

    base.main()


if __name__ == "__main__":
    main()
