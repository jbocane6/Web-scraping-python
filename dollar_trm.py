from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
# ignore warnings
import warnings


warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# conver web page table into dataframe.
url = "https://dolar.wilkinsonpc.com.co/divisas/dolar.html"
html = requests.get(url).content

dfs = pd.read_html(html)
for df in dfs:
    if "FECHA" in df.columns:
        # remove unnecesary columns
        df.drop(["VOLUMEN USD", "TRANSACCIONES",
                "VOLATILIDAD"], axis=1, inplace=True)
        days = {"lunes ", "martes ", "miércoles ",
                "jueves ", "viernes ", "sábado ", "domingo "}
        prefixes = {" de ", " del 2022"}
        months = {"enero": "/01", "febrero": "/02", "marzo": "/03",
                  "abril": "/04", "mayo": "/05", "junio": "/06",
                  "julio": "/07", "agosto": "/08", "septiembre": "/09",
                  "octubre": "/10", "noviembre": "/11", "diciembre": "/12"}

        for day in days:
            df["FECHA"] = df.FECHA.str.replace(day, "")
        for prefix in prefixes:
            df["FECHA"] = df.FECHA.str.replace(prefix, "")
            for month in months:
                df["FECHA"] = df.FECHA.str.replace(month, months[month])
        df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m")
        df["FECHA"] = df["FECHA"].dt.strftime("%m/%d")

        signs = {"COP ", "$", ","}
        for sign in signs:
            df["TRM"] = df.TRM.str.replace(sign, "")
        df["TRM"] = df["TRM"].astype(float)
        df = df.sort_values("FECHA")
        df.tail()

        plt.plot(df.FECHA, df.TRM)
        plt.scatter(df.FECHA, df.TRM, c="black")
        plt.grid()
        plt.title("Dólar TRM histórico", size=15)
        plt.xlabel("Fecha", size=15)
        plt.ylabel("TRM (COP $)", size=15)
        for x, y in zip(df.FECHA, df.TRM):
            label = "{:.1f}".format(y)
            plt.annotate(label,  # this is the text
                         (x, y),  # Coordinates to position the label
                         textcoords="offset points",  # Position of the text
                         xytext=(0, 5),  # distance from text to points (x,y)
                         ha="center", fontsize=8)  # h alignment and font size
        plt.show()
