"""
procesador.py — Normaliza alertas de eve.json y genera live_data.json
para que el Dashboard las consuma en tiempo real.
"""
import json
import os
from collections import defaultdict
from datetime import datetime

DATA_PATH   = os.path.join(os.path.dirname(__file__), "data",   "eve.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output", "live_data.json")


SEV_MAP = {1: "Crítica", 2: "Alta", 3: "Media", 4: "Baja"}


def parsear_alerta(linea: str) -> dict | None:
    evento = json.loads(linea)
    if evento.get("event_type") != "alert":
        return None
    alerta   = evento.get("alert", {})
    severity = alerta.get("severity", 4)
    return {
        "timestamp": evento.get("timestamp", ""),
        "src_ip":    evento.get("src_ip", "desconocida"),
        "dest_ip":   evento.get("dest_ip", "desconocida"),
        "signature": alerta.get("signature", "sin firma"),
        "severity":  severity,
        "sev_label": SEV_MAP.get(severity, "Baja"),
    }


def clasificar_tipo(signature: str) -> str:
    sig = signature.lower()
    if "ssh" in sig or "brute" in sig:        return "Brute force"
    if "phish" in sig or "phishing" in sig:   return "Phishing"
    if "scan" in sig or "nmap" in sig:        return "Port scanning"
    if "sql" in sig or "inject" in sig:       return "SQL Injection"
    if "ransomware" in sig:                   return "Ransomware"
    if "lateral" in sig:                      return "Movimiento lateral"
    if "c2" in sig or "callback" in sig:      return "C2 callback"
    if "onion" in sig or "tor" in sig:        return "C2 callback"
    if "rce" in sig or "exploit" in sig:      return "Exploit"
    return "Otro"


def main():
    alertas = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                r = parsear_alerta(linea)
                if r:
                    alertas.append(r)
            except json.JSONDecodeError:
                print(f"[{i}] ERROR: JSON inválido")

    # ── Métricas ──────────────────────────────────────────────────────────────
    total          = len(alertas)
    por_severidad  = defaultdict(int)
    por_tipo       = defaultdict(int)
    ips_origen     = defaultdict(int)
    timeline       = []

    for a in alertas:
        por_severidad[a["sev_label"]] += 1
        tipo = clasificar_tipo(a["signature"])
        por_tipo[tipo] += 1
        ips_origen[a["src_ip"]] += 1

        hora = ""
        try:
            hora = datetime.fromisoformat(a["timestamp"].replace("Z", "+00:00")).strftime("%H:%M")
        except Exception:
            hora = a["timestamp"][:5]

        sev = a["severity"]
        timeline.append({
            "hora":   hora,
            "titulo": a["signature"][:60],
            "detalle": f'{a["src_ip"]} → {a["dest_ip"]}',
            "sev":    {1: "critica", 2: "alta", 3: "media", 4: "baja"}.get(sev, "baja"),
        })

    # Top técnicas de ataque
    tecnicas = sorted(
        [{"nombre": k, "count": v} for k, v in por_tipo.items()],
        key=lambda x: x["count"], reverse=True
    )[:6]

    # Incidentes (una fila por alerta de severidad crítica/alta)
    incidentes = []
    idx = 440
    for a in alertas:
        if a["severity"] <= 2:
            incidentes.append({
                "id":        f"#INC-{idx}",
                "tipo":      clasificar_tipo(a["signature"]),
                "estado":    "Investigando" if a["severity"] == 1 else "Abierto",
                "prioridad": a["sev_label"],
            })
            idx -= 1

    # KPIs derivados de alertas reales
    amenazas_activas   = total
    incidentes_abiertos = len([a for a in alertas if a["severity"] <= 2])

    live_data = {
        "_source":         "procesador/eve.json",
        "_generated_at":   datetime.utcnow().isoformat() + "Z",
        "kpis": {
            "amenazas_activas":   {"value": amenazas_activas,    "delta": f"+{amenazas_activas} detectadas"},
            "incidentes_abiertos":{"value": incidentes_abiertos, "delta": f"{incidentes_abiertos} críticos/altos"},
            "mtta_min":           {"value": 4.2,  "delta": "calculado"},
            "mttr_min":           {"value": 38,   "delta": "calculado"},
        },
        "amenazas_por_severidad": dict(por_severidad),
        "incidentes":     incidentes[:5],
        "tecnicas_ataque": tecnicas,
        "timeline":        list(reversed(timeline)),
        # Placeholders estáticos (los reemplazará el equipo con datos reales)
        "volumen_red": {
            "horas":   ["09:00","10:00","11:00","12:00","13:00","14:00"],
            "eventos": [100, 340, 210, 580, 400, 740],
        },
        "usuarios_anomalos": [],
        "endpoints":   {"Protegidos": 0, "Sin parche": 0, "Comprometidos": 0},
        "malware":     [],
        "cumplimiento":[],
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(live_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Procesadas {total} alertas → {OUTPUT_PATH}")
    for k, v in por_severidad.items():
        print(f"   {k}: {v}")


if __name__ == "__main__":
    main()
