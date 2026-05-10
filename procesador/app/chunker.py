import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "playbook_sample.txt")
CHUNK_SIZE = 3  # líneas por fragmento

def chunk_texto(texto, chunk_size=CHUNK_SIZE):
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    chunks = []
    for i in range(0, len(lineas), chunk_size):
        chunk = " ".join(lineas[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = chunk_texto(texto)

    print(f"{len(chunks)} chunks generados del playbook:\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"[Chunk {i}] {chunk}\n")

if __name__ == "__main__":
    main()