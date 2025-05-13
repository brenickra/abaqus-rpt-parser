# -*- coding: utf-8 -*-
import re
import pandas as pd
from pathlib import Path

# === CONFIGURAÇÃO INICIAL ===
file = "linearStress_undeformed.rpt"  # Nome do arquivo .rpt (deve estar na mesma pasta)
stress_type = "Min."     # Escolha: Mises, Tresca, Max., Min., Mid.
normalized_stress_type = stress_type.rstrip('.')

# === LEITURA DO ARQUIVO ===
file_path = Path(file)
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Identificar índice da coluna correspondente ao stress_type
header_index = None
for line in lines:
    if "Max." in line and "Tresca" in line and "Mises" in line:
        headers = line.strip().split()
        clean_headers = [h.rstrip('.') for h in headers]
        if normalized_stress_type in clean_headers:
            header_index = clean_headers.index(normalized_stress_type)
            break

if header_index is None:
    raise RuntimeError(f"Cabeçalho com o tipo de tensão '{stress_type}' não encontrado.")

# === PARSER FINAL: Leitura direta linha por linha ===
results = []
current_lc = None
current_section = None
current_data = {}

label_map = {
    "(Average) Stress": "Pm",
    "Bending, Point 1": "Pm+Pb Point 1",
    "Bending, Point 2": "Pm+Pb Point 2",
    "Point 1": "Peak Point 1",
    "Point 2": "Peak Point 2",
}

for i, line in enumerate(lines):
    stripped_line = line.strip()

    if match := re.search(r"Step:\s+(\S+)", stripped_line):
        current_lc = match.group(1)

    if match := re.search(r"stress line '([^']+)'", stripped_line):
        if current_data and current_data.get("Load Case") and current_data.get("Section"):
            results.append(current_data)
        current_section = match.group(1)
        current_data = {
            "Load Case": current_lc,
            "Section": current_section,
            **{f"{v} ({normalized_stress_type})": None for v in label_map.values()}
        }

    for label_start, field in label_map.items():
        if stripped_line.startswith(label_start):
            try:
                parts = stripped_line.split()
                label_len = len(label_start.split())
                values_only = parts[label_len:]  # tudo após o nome do rótulo
                current_data[f"{field} ({normalized_stress_type})"] = float(values_only[header_index])
            except Exception:
                continue

# Finaliza último bloco
if current_data and current_data.get("Load Case") and current_data.get("Section"):
    results.append(current_data)

# === EXPORTA CSV ===
df = pd.DataFrame(results)
output_csv = file_path.with_name(f"{file_path.stem}_summary_{normalized_stress_type}.csv")
df.to_csv(output_csv, index=False)
print(f"Resumo exportado com sucesso para: {output_csv}")
print(df)
