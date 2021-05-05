import pandas as pd


def DescargarCSV():
    df = pd.read_csv("https://github.com/MinCiencia/Datos-COVID19/raw/master/output/producto3/TotalesPorRegion.csv")
    df.to_csv("archivo.csv")

    return

if __name__ == '__main__':
    DescargarCSV()