import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# --- Configurações ---
caminho_csv = r'D:\geoprojetos\data\cenfe\43_rs\43_RS.csv'
caminho_gpkg_saida = r'D:\geoprojetos\outputs\cenfe\43_rs.gpkg'
crs_sirgas2000 = 'EPSG:4674'
chunk_size = 1000  # Ajuste conforme memória disponível

# --- Verificação do CSV ---
if not os.path.exists(caminho_csv):
    print(f"❌ Erro: Arquivo CSV não encontrado: {caminho_csv}")
    exit()

print("📥 Iniciando leitura por chunks...")

chunks_validos = []
total_registros = 0
total_validos = 0

# --- Leitura em blocos ---
try:
    reader = pd.read_csv(caminho_csv, sep=';', dtype=str, chunksize=chunk_size, encoding='utf-8')

    for i, chunk in enumerate(reader):
        print(f"🔍 Processando chunk {i+1}...")

        chunk.columns = chunk.columns.str.strip()  # Garantir nomes limpos

        if 'LATITUDE' not in chunk.columns or 'LONGITUDE' not in chunk.columns:
            print("❌ Colunas de coordenadas não encontradas.")
            continue

        total_registros += len(chunk)

        # Converte e remove linhas inválidas
        chunk['LATITUDE'] = pd.to_numeric(chunk['LATITUDE'], errors='coerce')
        chunk['LONGITUDE'] = pd.to_numeric(chunk['LONGITUDE'], errors='coerce')
        chunk.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

        total_validos += len(chunk)

        # Cria geometria
        geometry = [Point(xy) for xy in zip(chunk['LONGITUDE'], chunk['LATITUDE'])]
        gdf_chunk = gpd.GeoDataFrame(chunk, geometry=geometry, crs=crs_sirgas2000)

        chunks_validos.append(gdf_chunk)

    # Junta tudo em um único GeoDataFrame
    if chunks_validos:
        gdf_total = gpd.GeoDataFrame(pd.concat(chunks_validos, ignore_index=True), crs=crs_sirgas2000)

        print("💾 Salvando como GeoPackage...")
        gdf_total.to_file(caminho_gpkg_saida, driver='GPKG')
        print(f"✅ Arquivo salvo com sucesso: {caminho_gpkg_saida}")
        print(f"🔢 Total original: {total_registros} registros.")
        print(f"📌 Total com coordenadas válidas: {total_validos} registros.")

    else:
        print("⚠️ Nenhum dado válido encontrado.")

except Exception as e:
    print(f"❌ Erro no processamento: {e}")


