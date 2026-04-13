import time
import importlib.metadata

DEPENDENCIAS = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "qdrant-client",
    "sentence-transformers",
]

def main():
    print("=" * 50)
    print("  CapacitaSOC - Capa 5: Procesador de Logs")
    print("=" * 50)
    print("\n[INFO] Dependencias instaladas:\n")

    for lib in DEPENDENCIAS:
        try:
            version = importlib.metadata.version(lib)
            print(f"  OK  {lib} == {version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"  ERROR  {lib} no encontrada")

    print("\n[INFO] Entorno listo para Sprint 2.")
    print("[INFO] Contenedor ejecutandose de forma estable...\n")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
