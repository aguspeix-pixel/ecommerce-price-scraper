import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL_OBJETIVO = "https://books.toscrape.com/catalogue/page-1.html"

def extraer_productos(url):
    print(f"🌐 Conectando a {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    respuesta = requests.get(url, headers=headers, timeout=15)
    respuesta.raise_for_status()

    sopa = BeautifulSoup(respuesta.text, "html.parser")
    articulos = sopa.find_all("article", class_="product_pod")

    mapa_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    fecha_extraccion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    productos = []

    for item in articulos:
        titulo = item.h3.a["title"].strip()
        precio_texto = item.find("p", class_="price_color").text.strip()
        precio_limpio = float("".join(c for c in precio_texto if c.isdigit() or c == "."))
        disponibilidad = item.find("p", class_="instock availability").text.strip()
        clase_rating = item.find("p", class_="star-rating")["class"][1]
        rating = mapa_rating.get(clase_rating, 0)

        productos.append({
            "Fecha_Extraccion": fecha_extraccion,
            "Producto": titulo,
            "Precio_GBP": precio_limpio,
            "Rating": rating,
            "Disponibilidad": disponibilidad
        })

    return pd.DataFrame(productos)

def guardar_y_reportar(df):
    conexion = sqlite3.connect("monitoreo_precios.db")
    df.to_sql("historial_precios", conexion, if_exists="append", index=False)

    query_ofertas = """
        SELECT 
            Producto,
            Precio_GBP,
            Rating,
            Disponibilidad
        FROM historial_precios
        WHERE Precio_GBP < 20.0
        ORDER BY Precio_GBP ASC;
    """
    df_ofertas = pd.read_sql_query(query_ofertas, conexion)
    conexion.close()

    archivo_excel = "Reporte_Monitoreo_Precios.xlsx"
    with pd.ExcelWriter(archivo_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Catalogo_Completo", index=False)
        df_ofertas.to_excel(writer, sheet_name="Alertas_Precio_Bajo", index=False)

    print(f"✅ {len(df)} productos extraídos y guardados en 'monitoreo_precios.db'")
    print(f"🔥 {len(df_ofertas)} oportunidades detectadas (< £20.00)")
    print(f"📑 Excel generado: '{archivo_excel}'")

if __name__ == "__main__":
    df_datos = extraer_productos(URL_OBJETIVO)
    guardar_y_reportar(df_datos)