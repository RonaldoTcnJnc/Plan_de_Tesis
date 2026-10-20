import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SERVICE_URL = (
    "https://services6.arcgis.com/lMIZrqiJkpM748BR/arcgis/rest/services/"
    "SIDPOL_DELITOS_TOTAL/FeatureServer/1/query"
)
OUTPUT = Path(__file__).with_name("sidpol_cusco.csv")
FIELDS = [
    "OBJECTID",
    "ID_DGC_03",
    "fecha_hora_hecho",
    "turno_hecho",
    "año_hecho",
    "mes_hecho",
    "dia_hecho",
    "ubigeo_hecho_delito",
    "lat_hecho",
    "long_hecho",
    "departamento_hecho",
    "provincia_hecho",
    "distrito_hecho",
    "solo_denuncia",
    "materia_hecho",
    "tipo_hecho",
    "subtipo_hecho",
    "modalidad_hecho",
    "fuente",
    "FIABILIDAD",
    "ESTADO_COORD",
]
WHERE = "departamento_hecho='CUSCO'"
PAGE_SIZE = 2000


def fetch_page(offset):
    params = {
        "where": WHERE,
        "outFields": ",".join(FIELDS),
        "returnGeometry": "false",
        "orderByFields": "OBJECTID",
        "resultOffset": offset,
        "resultRecordCount": PAGE_SIZE,
        "f": "json",
    }
    request = Request(
        f"{SERVICE_URL}?{urlencode(params)}",
        headers={"User-Agent": "tesis-sidpol-data-retrieval/1.0"},
    )
    with urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload


def main():
    count_params = {
        "where": WHERE,
        "returnCountOnly": "true",
        "f": "json",
    }
    count_request = Request(
        f"{SERVICE_URL}?{urlencode(count_params)}",
        headers={"User-Agent": "tesis-sidpol-data-retrieval/1.0"},
    )
    with urlopen(count_request, timeout=60) as response:
        expected_count = json.load(response)["count"]

    offset = 0
    downloaded = 0
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        while offset < expected_count:
            page = fetch_page(offset)
            features = page.get("features", [])
            if not features:
                break
            writer.writerows(feature["attributes"] for feature in features)
            downloaded += len(features)
            offset += len(features)
            print(f"Descargados: {downloaded}/{expected_count}")

    if downloaded != expected_count:
        raise RuntimeError(
            f"Descarga incompleta: se esperaban {expected_count} registros y "
            f"se recibieron {downloaded}."
        )
    print(f"Archivo guardado: {OUTPUT}")


if __name__ == "__main__":
    main()