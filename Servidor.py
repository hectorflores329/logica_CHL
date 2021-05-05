import os
import shutil
import subprocess
import shutil
import os
import stat
from os import path
import time
import datetime
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import pandas as pd
import numpy as np
import dateparser
from zipfile import ZipFile
import requests


def DescargarCSV():
    df = pd.read_csv("https://github.com/MinCiencia/Datos-COVID19/raw/master/output/producto3/TotalesPorRegion.csv")
    df.to_csv("archivo.csv")


if __name__ == '__main__':
    print('Empezando proceso de descarga.')
    DescargarCSV()
    print('El roceso de descarga ha finalizado.')