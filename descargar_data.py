import yfinance as yf
import pandas as pd
import os

# Crear carpeta para guardar los datos
os.makedirs("data", exist_ok=True)

print("Descargando datos de XAUUSD (Oro)...")
oro = yf.download("GC=F", start="2022-01-01", end="2024-12-31", interval="1d")
oro.to_csv("data/XAUUSD_diario.csv")
print(f"✓ Oro: {len(oro)} velas guardadas")

print("Descargando datos de Nasdaq...")
nasdaq = yf.download("NQ=F", start="2022-01-01", end="2024-12-31", interval="1d")
nasdaq.to_csv("data/NASDAQ_diario.csv")
print(f"✓ Nasdaq: {len(nasdaq)} velas guardadas")

print("\n¡Listo! Archivos guardados en la carpeta 'data'")