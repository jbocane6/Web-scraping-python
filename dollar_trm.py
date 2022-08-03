 ## importar paquetes necesarios
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
## ignorar las advertencias
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
### convertir table de pagina web en un dataframe.
url = "https://dolar.wilkinsonpc.com.co/divisas/dolar.html"
html = requests.get(url).content
df = pd.read_html(html)
df = df[19]
## eliminar columnas innecesarias
df.drop(["VOLUMEN USD", "TRANSACCIONES", "VOLATILIDAD"], axis = 1, inplace = True)
df["TRM"] = df.TRM.str.replace('^[-+]?[0-9]+$', '')
df["FECHA"] =df.FECHA.str.replace("lunes ","")
df["FECHA"] =df.FECHA.str.replace("martes ","")
df["FECHA"] =df.FECHA.str.replace("miércoles ","")
df["FECHA"] =df.FECHA.str.replace("jueves ","")
df["FECHA"] =df.FECHA.str.replace("viernes ","")
df["FECHA"] =df.FECHA.str.replace("sábado ","")
df["FECHA"] =df.FECHA.str.replace("domingo ","")
df["FECHA"] =df.FECHA.str.replace(" de agosto del 2022","/08")
df["FECHA"] = df.FECHA.str.replace(" de julio del 2022","/07")
df["FECHA"] = pd.to_datetime(df["FECHA"], format='%d/%m')
df["FECHA"] = df["FECHA"].dt.strftime('%m/%d')
df["TRM"] = df.TRM.str.replace('COP ', '')
df["TRM"] = df.TRM.str.replace('$', '')
df["TRM"] = df.TRM.str.replace(',', '')
df["TRM"] = df["TRM"].astype(float)
df = df.sort_values("FECHA")
df.tail()

plt.plot(df.FECHA, df.TRM)
plt.scatter(df.FECHA, df.TRM, c = "black")
plt.grid()
plt.title("Dólar TRM histórico")
plt.xlabel("Fecha")
plt.ylabel("TRM (COP $)")
plt.show()
