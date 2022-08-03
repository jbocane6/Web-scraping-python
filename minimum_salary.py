 ## importar paquetes necesarios
import requests
import pandas as pd
import matplotlib.pyplot as plt
## ignorar las advertencias
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
### convertir table de pagina web en un dataframe.
url = "https://www.salariominimocolombia.net/historico/"
html = requests.get(url).content
df = pd.read_html(html)
df = df[0]
## vemos las primeras 5 obs
df.head(5)
## eliminar la columna Años y acción
df.drop(["Año", "Acción"], axis = 1, inplace = True)
## cambiar nombre de la columna salario
df = df.rename(columns={"Salario Mínimo(Pesos Colombianos)":"salario"})
## eliminar primera fila
df = df.drop(index = 0)
df.head()
años = list(range(2022, 1983, -1))
df["años"] = años
df.head()
df["salario"] = df.salario.str.replace('^[-+]?[0-9]+$', '')
df["salario"] = df.salario.str.replace('$', '')
df["salario"] = df.salario.str.replace(',', '')
df["salario"] = df["salario"].astype(int)
df.head()
plt.plot(df.años, df.salario)
plt.scatter(df.años, df.salario, c = "red")
plt.ticklabel_format(style='plain')
plt.grid()
plt.title("Salario minimo colombiano historico")
plt.xlabel("Año")
plt.ylabel("Salario")
plt.show()