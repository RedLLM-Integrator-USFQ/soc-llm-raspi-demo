import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "eve.json")

def parsear_alerta(linea):
    evento = json.loads(linea)

    if evento.get("event_type") != "alert":
        return None

    src_ip    = evento.get("src_ip", "desconocida")
    dest_ip   = evento.get("dest_ip", "desconocida")
    alerta    = evento.get("alert", {})
    signature = alerta.get("signature", "sin firma")
    severity  = alerta.get("severity", "?")

    return f"Alerta de severidad {severity}: Se detectó {signature} desde la IP {src_ip} hacia la IP {dest_ip}"

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                resultado = parsear_alerta(linea)
                if resultado:
                    print(f"[{i}] {resultado}")
            except json.JSONDecodeError:
                print(f"[{i}] ERROR: línea no es JSON válido")

    print()
    print("Normalización completada.")

if __name__ == "__main__":
    main()
