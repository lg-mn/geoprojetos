# Le um shapefile de um estado, plota o mapa, filtra um município e o exporta como gpkg
import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path = r'D:\projetos\data\shapefiles\brasil\RS_Municipios_2024\sul\rs\RS_Municipios_2024.shp'#mapa do arquivo com shapefiles, deve ser definido
gdf = gpd.read_file(shapefile_path)

#print(gdf.head())  # Verifica se o shapefile foi lido corretamente


gdf.plot(figsize=(10,10), edgecolor='black')
plt.title("Malha municipal do Rio Grande do Sul")
plt.show()

municipio_nome = input("Digite o Nome do Município que deseja Filtrar: ") #pode melhorar, fazer uma lista ou algo parecido

municipio_filtrado = gdf[gdf["NM_MUN"] == municipio_nome] #pode melhorar, o usuario deve digitar exatamente

if municipio_filtrado.empty:
    print(f"Município '{municipio_nome}' não encontrado!") #pode melhorar, o sistema deve deixar tentar de novo
else:
    municipio_filtrado.plot(figsize=(8,8), edgecolor='black', color='lightblue') #plota o mapa do municipio
    plt.title(f"Município de {municipio_nome}")
    plt.show()
    output_path = rf'D:\projetos\outputs\shapefiles\brasil\sul\rs\{municipio_nome}.gpkg' #exporta um shape do municipio
    municipio_filtrado.to_file(output_path, driver="GPKG")
    print(f"Arquivo {municipio_nome}.gpkg salvo em {output_path}")