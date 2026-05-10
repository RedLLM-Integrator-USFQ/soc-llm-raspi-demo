import json
import os
from procesador import parsear_alerta, formatear_texto
from chunker import chunk_texto

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "eve.json")
PLAYBOOK_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "playbook_sample.txt")

# TODO: Ahmed debe ejecutar db/init_qdrant.py primero para que las colecciones 'incidentes_historicos' y 'soc_playbooks' existan en Qdrant.

def conectar_qdrant():
    from qdrant_client import QdrantClient
    return QdrantClient(host="localhost", port=6333)

def ingestar_logs():
    # TODO: Reemplazar print por insercion real en Qdrant cuando Ahmed confirme que las colecciones estan listas.
    print("--- Ingesta de logs Suricata ---")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                log = parsear_alerta(linea)
                if log:
                    texto = formatear_texto(log)
                    print(f"[Log {i}] Listo para vectorizar: {texto}")
            except json.JSONDecodeError:
                print(f"[Log {i}] ERROR: linea no es JSON valido")

def ingestar_playbooks():
    # TODO: Reemplazar print por insercion real en Qdrant cuando Ahmed confirme que las colecciones estan listas.
    print("\nIngesta de Playbooks")
    with open(PLAYBOOK_PATH, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = chunk_texto(texto)
    for i, chunk in enumerate(chunks, 1):
        print(f"[Chunk {i}] Listo para vectorizar: {chunk}")

def main():
    ingestar_logs()
    ingestar_playbooks()
    print("\nPipeline completado")

if __name__ == "__main__":
    main()