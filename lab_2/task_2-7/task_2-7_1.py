files = ["seq1", "seq2", "seq3", "seq4"]

sample_date = "2026-02-19"

print(f" Фиксированная дата взятия образцов: {sample_date}")

for name in files:
    new_name = f"{name}_{sample_date}.fasta"
    print(f" {new_name}")
