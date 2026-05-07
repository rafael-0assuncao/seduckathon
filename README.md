import ee
import folium

# 1. AUTENTICAÇÃO E INICIALIZAÇÃO
# O ID do projeto foi extraído da sua imagem image_e55fdb.jpg
ee.Authenticate()
meu_projeto_id = 'piaui-carbono-social-495415'
ee.Initialize(project=meu_projeto_id)

# 2. CONFIGURAÇÃO DA LOCALIZAÇÃO (ASSENTAMENTO 17 DE ABRIL)
# Coordenadas precisas que você forneceu do assentamento
lat_final = -5.299992577304816
lon_final = -42.74356702850177
ponto_assentamento = ee.Geometry.Point([lon_final, lat_final])
area_focada = ponto_assentamento.buffer(2500)

# 3. COLETA DE DADOS DE SATÉLITE (SENTINEL-2)
imagem = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(area_focada) \
    .filterDate('2024-01-01', '2026-05-05') \
    .sort('CLOUDY_PIXEL_PERCENTAGE') \
    .first()

# 4. CÁLCULO DO NDVI (ÍNDICE DE VEGETAÇÃO)
ndvi = imagem.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(area_focada)

# Extração da média para o relatório de Carbono (Seu índice foi 0.5972 conforme log anterior)
media_ndvi = ndvi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=area_focada,
    scale=10
).getInfo()

print(f"📊 Índice médio de vegetação no Assentamento: {media_ndvi['NDVI']:.4f}")

# 5. TREINAMENTO DA IA (RANDOM FOREST) COM FILTRO DE SEGURANÇA
# Adicionando mais pontos para garantir que o erro "No valid training data" não ocorra
pontos_treino = ee.FeatureCollection([
    ee.Feature(ee.Geometry.Point([-42.7435, -5.2999]), {'classe': 1}), # Floresta/Verde
    ee.Feature(ee.Geometry.Point([-42.7450, -5.3010]), {'classe': 0}), # Solo/Construção
    ee.Feature(ee.Geometry.Point([-42.7420, -5.2985]), {'classe': 1}), # Exemplo adicional Verde
    ee.Feature(ee.Geometry.Point([-42.7445, -5.3020]), {'classe': 0})  # Exemplo adicional Solo
])

# Amostragem com remoção de valores nulos (Evita o erro 400 que você recebeu)
treinamento = imagem.sampleRegions(
    collection=pontos_treino,
    properties=['classe'],
    scale=10,
    tileScale=16
).filter(ee.Filter.notNull(imagem.bandNames()))

# Verifica se os dados de treino são válidos antes de criar o classificador
if treinamento.size().getInfo() > 0:
    classificador = ee.Classifier.smileRandomForest(10).train(
        features=treinamento,
        classProperty='classe',
        inputProperties=imagem.bandNames()
    )
    # Aplicando a IA treinada
    classificado = imagem.classify(classificador).clip(area_focada)
    print("✅ IA treinada e aplicada à área das 84 famílias com sucesso.")
else:
    print("❌ Erro: Pontos de treino sem dados válidos. O mapa mostrará apenas o NDVI.")
    classificado = None

# 6. CONFIGURAÇÃO DO MAPA INTERATIVO (FOLIUM)
mapa_final = folium.Map(location=[lat_final, lon_final], zoom_start=15)

# Parâmetros de visualização
vis_params_ndvi = {'min': 0, 'max': 0.8, 'palette': ['#d73027', '#fee08b', '#1a9850']}
vis_params_ia = {'min': 0, 'max': 1, 'palette': ['#ff0000', '#006400']} # Vermelho para solo, Verde Escuro para floresta

# Camada 1: Mapa de Calor (NDVI)
map_id_ndvi = ndvi.getMapId(vis_params_ndvi)
folium.TileLayer(
    tiles=map_id_ndvi['tile_fetcher'].url_format,
    attr='Google Earth Engine',
    overlay=True,
    name='Saúde da Vegetação (NDVI)',
).add_to(mapa_final)

# Camada 2: Resultado da IA (Se o classificador funcionou)
if classificado:
    map_id_ia = classificado.getMapId(vis_params_ia)
    folium.TileLayer(
        tiles=map_id_ia['tile_fetcher'].url_format,
        attr='IA Piauí Carbono',
        overlay=True,
        name='Resultado da IA (Classificação)',
    ).add_to(mapa_final)

# Marcador no Assentamento
folium.Marker([lat_final, lon_final], popup="Assentamento 17 de Abril").add_to(mapa_final)

# Controle de Camadas (Importante para alternar entre NDVI e IA)
folium.LayerControl().add_to(mapa_final)

# EXIBIR MAPA
mapa_final
