import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "eve.json")

def normalizar_severidad(nivel):
    mapa = {
        1: "critica",
        2: "alta",
        3: "media",
        4: "baja"
    }
    return mapa.get(nivel, "desconocida")

def normalizar_timestamp(ts_raw):
    try:
        dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return "timestamp_invalido"

def parsear_alerta(linea):
    evento = json.loads(linea)

    if evento.get("event_type") != "alert":
        return None

    alerta = evento.get("alert", {})

    return {
        "timestamp": normalizar_timestamp(evento.get("timestamp", "")),
        "src_ip": evento.get("src_ip", "desconocida"),
        "dest_ip": evento.get("dest_ip", "desconocida"),
        "signature": alerta.get("signature", "sin firma"),
        "severidad": normalizar_severidad(alerta.get("severity")),
        "tipo_ataque": alerta.get("category", "desconocido")
    }

def formatear_texto(log):
    return (
        f"Alerta de severidad {log['severidad']}: "
        f"Se detecto {log['signature']} "
        f"desde {log['src_ip']} hacia {log['dest_ip']} "
        f"a las {log['timestamp']}. "
        f"Categoria: {log['tipo_ataque']}"
    )

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                log = parsear_alerta(linea)
                if log:
                    print(f"[{i}] {formatear_texto(log)}")
            except json.JSONDecodeError:
                print(f"[{i}] ERROR: linea no es JSON valido")

    print("\nNormalizacion completada.")

if __name__ == "__main__":
    main()