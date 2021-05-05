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

def Ciclo():
    print("Comenzo el Ciclo")
    print("***********************************************************************************************")
    print(datetime.datetime.now().strftime("                                 %m-%d-%Y %H:%M:%S"))
    print("***********************************************************************************************")
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Paso_a_paso/paso_a_paso.csv"
    ruta = "paso_a_paso/paso_a_paso.csv"
    DescargarCSV(url,ruta)
    cargarInOutPut()


def cargarInOutPut2():
    try:
        shutil.rmtree('input')
        #shutil.rmtree('../Datos_Chile/output')
    except:
        print("Error al borrar")
    url = 'https://codeload.github.com/MinCiencia/Datos-COVID19/zip/master'
    myfile = requests.get(url)
    open('proyecto.zip', 'wb').write(myfile.content)
    with ZipFile('proyecto.zip', 'r') as zipObj:
    # Extract all the contents of zip file in current directory
        zipObj.extractall()
    shutil.copytree("Datos-COVID19-master/input", "input", symlinks=False, ignore=None,  ignore_dangling_symlinks=False)
    #shutil.copytree("Datos-COVID19-master/output", "../Datos_Chile/output", symlinks=False, ignore=None,  ignore_dangling_symlinks=False)
    shutil.rmtree("Datos-COVID19-master")
    
    return

def cargarInOutPut():
    """
    try:
        try:
            os.mkdir("repo")
        except:
            for root, dirs, files in os.walk("repo"):  
                for dir in dirs:
                    os.chmod(path.join(root, dir), stat.S_IRWXU)
                for file in files:
                    os.chmod(path.join(root, file), stat.S_IRWXU)
            shutil.rmtree('repo')
        repo = git.Repo.clone_from("https://github.com/MinCiencia/Datos-COVID19", os.path.abspath(".") + "/repo")
        try:
            shutil.rmtree('../Datos_Chile/input')
            shutil.rmtree('../Datos_Chile/output')
        except:
            print("Error al borrar")
        shutil.copytree("repo/input", "../Datos_Chile/input")
        shutil.copytree("repo/output", "../Datos_Chile/output")
        for root, dirs, files in os.walk("repo"):  
            for dir in dirs:
                os.chmod(path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(path.join(root, file), stat.S_IRWXU)
        shutil.rmtree('repo')
        #guardarRepositorio()
        #return True

    except:
        print("Error en el proceso")
        #return False
    """
    
    try:
        cargarInOutPut2()
        print("Documentos Guardados")
    except:
        print("Error en Documentos Guardados")
    try:
        CalculosParaChile()
        print("Calculos para Chile Finalizo correctamente")
    except:
        print("Error en Calculos para Chile")
    # guardarRepositorio()
    """
    for i in range(12):        
        try:
            print("***********************************************************************************************")
            print(datetime.datetime.now().strftime("                                 %m-%d-%Y %H:%M:%S"))
            print("***********************************************************************************************")
            #Validar()
            ResumenRegional2()
            guardarRepositorio()
            print("Resumen regional actualizado")
        except:
            print("Error en resumen regional")
        time.sleep(60 * 60 * 12) 
    """
    ResumenRegional2()
    # guardarRepositorio()
    print("Resumen regional actualizado")
    # guardarRepositorio()
    return

def limpieza(data):    
    # ***********************************************************************
    # 1 aca debiese trabajar el ciclo for al integrar segundafuncion(i) a la funcionglobal().
    # 2 data = primerafuncion() debe estar en la funcionglobal() fuera del ciclo for.
    # 3 la línea: CD_Corr_unique = np.unique(data['CD_Corr']) debe salir de acá.
    # e incluirse fuera del ciclo for en la funcionglobal().
    # ***********************************************************************
    our_data_filter = data[['Comuna','Fecha','Nuevos','Nuevos Fallecidos','Nuevos Recuperados','Poblacion']]
    our_data_filter = our_data_filter.fillna(0)
    our_data_filter['NuevosConfirmados'] = pd.to_numeric(our_data_filter['Nuevos'])
    our_data_filter['NuevosFallecidos'] = pd.to_numeric(our_data_filter['Nuevos Fallecidos'])
    our_data_filter['NuevosRecuperados'] = pd.to_numeric(our_data_filter['Nuevos Recuperados'])
    our_data_filter['Poblacion'] = pd.to_numeric(our_data_filter['Poblacion'])

    #eliminamos la primera fila que es un NA
    #our_data_filter = our_data_filter.iloc[1:]

    our_data_filter['NuevosConfirmados'] = our_data_filter['NuevosConfirmados'] + our_data_filter['NuevosFallecidos']
    our_data_filter['NuevosConfirmadosacum'] = our_data_filter['NuevosConfirmados'].cumsum()
    our_data_filter['NuevosRecuperadosacum'] = our_data_filter['NuevosRecuperados'].cumsum()
    our_data_filter["Susceptibles"] = our_data_filter['Poblacion'] - our_data_filter['NuevosConfirmadosacum'] - our_data_filter['NuevosRecuperadosacum']
    our_data_filter["pob_log_Susceptibles"] = our_data_filter['Poblacion'] * np.log(our_data_filter["Susceptibles"])

    # extraemos un subconjunto que llegue solo hasta el dia de hoy:
    #now = datetime.datetime.now()
    #our_data_filter_un = our_data_filter[our_data_filter['Fecha'] < now]
    our_data_filter_un = our_data_filter 
    # filtramos desde el primer dia en el que haya recuperados:
    our_data_filter_un_final = our_data_filter_un[our_data_filter_un['NuevosRecuperadosacum'] > 0]
    
    #y = our_data_filter_un_final["pob_log_Susceptibles"]

    return(our_data_filter_un_final)

def calculorR0(data2):    
    # declaramos una lista para almacenar los R0:
    lista_R0 = []
    
    # Reemplazamos los NA por 0:
    data2.fillna("0", inplace = True) 
    
    y = data2["pob_log_Susceptibles"]
    for i in range(len(y)):
        try:
            y = data2["pob_log_Susceptibles"]
            x = data2["NuevosRecuperadosacum"]
            yy = y.head(i+1)
            xx = x.head(i+1)
            # print(xx)
            # print(yy)
            # Creamos el objeto de Regresión Lineal
            regresion_lineal = linear_model.LinearRegression()

            regresion_lineal.fit(xx.values.reshape(-1, 1),yy.values.reshape(-1, 1))
            r0 = -regresion_lineal.coef_
            lista_R0.append(r0[0][0])
            
        except:
            #print("Error")
            lista_R0.append(0)
            
    data2["r0"] = lista_R0
    salida = data2[["Comuna","Fecha", "r0"]]
    return(salida)

def CalculosParaChile():
    #linkFallecidos = "https://raw.githubusercontent.com/Sud-Austral/Datos_Chile/master/output/producto38/CasosFallecidosPorComuna.csv"
    #linkAcumulados = "https://raw.githubusercontent.com/Sud-Austral/Datos_Chile/master/input/InformeEpidemiologico/CasosAcumuladosPorComuna.csv"
    #linkActivos = "https://raw.githubusercontent.com/Sud-Austral/Datos_Chile/master/output/producto19/CasosActivosPorComuna.csv"

    linkFallecidos = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna.csv"
    linkAcumulados = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/InformeEpidemiologico/CasosAcumuladosPorComuna.csv"
    linkActivos = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv"

    dataFallecido = pd.read_csv(linkFallecidos)
    dataAcumulado = pd.read_csv(linkAcumulados)
    dataActivo = pd.read_csv(linkActivos)

    dataFallecido = dataFallecido.fillna(0) 
    dataAcumulado = dataAcumulado.fillna(0)
    dataActivo = dataActivo.fillna(0)

    comunas = dataActivo["Comuna"].unique().tolist()
    comunas.remove('Total')

    salida = []

    for comuna in comunas:
        #print(comuna)
        auxActivo = dataActivo[dataActivo["Comuna"] == comuna]
        auxdataFallecido = dataFallecido[dataFallecido["Comuna"] == comuna]
        auxdataAcumulado = dataAcumulado[dataAcumulado["Comuna"] == comuna]
        id_ = auxActivo.columns[:5].tolist()
        value = auxActivo.columns[5:].tolist()
        auxActivoMelt = pd.melt(auxActivo, id_vars=id_, value_vars=value)
        auxActivoMelt["Fecha"] = auxActivoMelt["variable"]
        auxActivoMelt["Activo"] = auxActivoMelt["value"]
        del auxActivoMelt["variable"]
        del auxActivoMelt["value"]
        ###################################################################
        id_ = auxdataFallecido.columns[:5].tolist()
        value = auxdataFallecido.columns[5:].tolist()
        auxdataFallecidoMelt = pd.melt(auxdataFallecido, id_vars=id_, value_vars=value)
        auxdataFallecidoMelt["Fecha"] = auxdataFallecidoMelt["variable"]
        auxdataFallecidoMelt["Fallecido"] = auxdataFallecidoMelt["value"]
        del auxdataFallecidoMelt["variable"]
        del auxdataFallecidoMelt["value"]
        ###################################################################
        id_ = auxdataAcumulado.columns[:5].tolist()
        value = auxdataAcumulado.columns[5:-1].tolist()
        auxdataAcumuladoMelt = pd.melt(auxdataAcumulado, id_vars=id_, value_vars=value)
        auxdataAcumuladoMelt["Fecha"] = auxdataAcumuladoMelt["variable"]
        auxdataAcumuladoMelt["Acumulado"] = auxdataAcumuladoMelt["value"]
        del auxdataAcumuladoMelt["variable"]
        del auxdataAcumuladoMelt["value"]

        columnas = auxdataAcumuladoMelt.columns[:6].tolist()
        semiMerge = auxdataAcumuladoMelt.merge(auxActivoMelt, left_on=columnas, right_on=columnas, how='outer')
        finalMerge = semiMerge.merge(auxdataFallecidoMelt,left_on=columnas, right_on=columnas, how='outer')
        finalMerge = finalMerge.fillna(0)
        #################################################################################
        lista = finalMerge['Acumulado'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        finalMerge['AcumuladoAux'] = lista
        finalMerge["Nuevos"] = finalMerge["Acumulado"] - finalMerge["AcumuladoAux"] 
        del finalMerge["AcumuladoAux"]
        
        #################################################################################
        lista = finalMerge['Fallecido'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        finalMerge['FallecidosAux'] = lista
        finalMerge["Nuevos Fallecidos"] = finalMerge["Fallecido"] - finalMerge["FallecidosAux"]    
        del finalMerge['FallecidosAux']

        corregir = finalMerge
        idx = 0
        acumulados = corregir["Acumulado"].tolist()
        activos = corregir["Activo"].tolist()
        for i in corregir["Activo"].tolist():
            if(i == 0):
                activos[idx] = acumulados[idx]
            else:
                break
            idx = idx + 1
            
        corregir["Activo"] = activos
        #################################################################################
        lista = corregir['Activo'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        corregir['ActivoAux'] = lista
        corregir["Nuevos Activo"] = finalMerge["Activo"] - finalMerge["ActivoAux"]    
        del corregir['ActivoAux']
        ##################################################################
        corregir["% Fallecido"] = corregir["Fallecido"] / corregir["Acumulado"]
        corregir["% Activo"] = corregir["Activo"] / corregir["Acumulado"]
        ##################################################################
        corregir["% Nuevo Casos"] = corregir["Nuevos"] / corregir["Acumulado"]
        corregir["% Nuevos Fallecido"] = corregir["Nuevos Fallecidos"] / corregir["Fallecido"]
        corregir["% Nuevos Activo"] = corregir["Nuevos Activo"] / corregir["Activo"]
        ################################################################################
        corregir["Recuperados"] = corregir["Acumulado"] -corregir["Fallecido"] - corregir["Activo"]
        lista = corregir['Recuperados'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        corregir['RecuperadosAux'] = lista
        corregir["Nuevos Recuperados"] = finalMerge["Recuperados"] - finalMerge["RecuperadosAux"]
        del corregir['RecuperadosAux']
        ###########################################################################################
        corregir["% Recuperados"] = corregir["Recuperados"] / corregir["Acumulado"]
        corregir["% Nuevos Recuperados"] = corregir["Nuevos Recuperados"] / corregir["Recuperados"]
        
        corregir["Recuperados/1MM hab"] = corregir["Recuperados"] * 1000000 / corregir["Poblacion"]
        corregir["Casos/1MM hab"] = corregir["Acumulado"] * 1000000 / corregir["Poblacion"]
        corregir["Fallecidos/1MM hab"] = corregir["Fallecido"] * 1000000 / corregir["Poblacion"]
        corregir["Activos/1MM hab"] = corregir["Activo"] * 1000000 / corregir["Poblacion"]
        listo = calculorR0(limpieza(corregir))
        corregir = corregir.merge(listo,left_on=["Comuna","Fecha"], right_on =["Comuna","Fecha"], how='outer' )
        final = corregir[["Region", 
                        "Codigo region", 
                        "Comuna", 
                        "Codigo comuna", 
                        "Poblacion", 
                        "Fecha", 
                        "Acumulado", 
                        "Nuevos", 
                        "Fallecido", 
                        "Nuevos Fallecidos", 
                        "Activo", 
                        "Nuevos Activo",
                        "Recuperados",
                        "Nuevos Recuperados",
                        "% Fallecido",
                        "% Activo",
                        "% Recuperados",
                        "% Nuevo Casos",
                        "% Nuevos Fallecido",
                        "% Nuevos Activo",
                        "% Nuevos Recuperados",
                        "Casos/1MM hab",
                        "Fallecidos/1MM hab",
                        "Activos/1MM hab",
                        "Recuperados/1MM hab",
                        "r0"
                        ]]
        #final = final.fillna(0)
        #final = final.replace([np.inf, -np.inf], 0)
        salida.append(final)
        #corregir.to_csv("test.csv", mode = "a", index= False, header=False)
        #print(comuna)
        #print(corregir.columns.tolist())
        #print("**************************************************************************************")
    result = pd.concat(salida)
    result = result.fillna(0)
    result = result.replace([np.inf, -np.inf], 0)
    result.to_csv("test.csv", index= False)
    #result
    #corregir
    #final
    result.to_csv("propios/Salida.csv", index= False)
    pd.read_csv("test.csv", index_col=False).to_excel("propios/Salida.xlsx", index=False)
    return None


###################################################################################################################################################################
def ArchivoOriginal():
    return pd.read_excel("Archivo_original.xlsx")

def FechaMaxima(data = ArchivoOriginal()):
    return data["Fecha Final"].max().strftime("%d-%m-%Y")

def cambiarRegion(region):
    salida = region
    if(salida == 'Araucanía'):
        salida = 'La Araucanía'
    if(salida == 'RM'):
        salida = 'Metropolitana'
    if(salida == 'Desconocida'):
        salida = 'No Informada'
    if(salida == 'O’Higgins'):
        salida = "O'Higgins"
    return salida

def Actualizar():
    dataPDF = pd.read_html("https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/")
    diaActual = dateparser.parse(dataPDF[0][1][0].split("Chile")[1][1:])

    dataWeb = pd.read_html("https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/", skiprows=1)
    data2 = dataWeb[0]
    data2.columns = data2.iloc[0]

    data2 = data2.reindex(data2.index.drop(0))
    #data2["Region"] = data2["nan"]
    data2.columns = ['Region',
                 'Casos confirmados acumulados',
                         'Casos nuevos totales',
                    'Casos nuevos con síntomas',
                  'Casos nuevos sin síntomas *',
                'Casos nuevos sin notificar **',
                    'Casos activos confirmados',
                       'Fallecidos totales ***',
           'Casos confirmados recuperados ****']
    data2['Region'] = data2['Region'].apply(cambiarRegion)
    data2 = data2[data2["Region"] != "Total"]
    data2["Fecha Final"] = diaActual
    data2["FechaNumber"] = diaActual.strftime("%d-%m-%Y")
    data2["Fecha"] = data2["Fecha Final"].apply(diaMes)
    aux = data2
    aux["Suma de Casos Acumulados"]   = aux["Casos confirmados acumulados"]
    aux["Suma de Casos Diarios"] = aux["Casos nuevos totales"]
    aux["Suma de Casos Activos"]  = aux["Casos activos confirmados"]
    aux["Suma de Recuperados"]  = aux["Casos confirmados recuperados ****"]
    aux["Suma de Muertes"] = aux["Fallecidos totales ***"]
    #******************************************************************
    del aux["Casos confirmados acumulados"]
    del aux["Casos nuevos totales"]
    del aux["Casos activos confirmados"]
    del aux["Casos confirmados recuperados ****"]
    del aux["Fallecidos totales ***"]
    
    del aux["Casos nuevos con síntomas"]
    del aux["Casos nuevos sin síntomas *"]
    del aux["Casos nuevos sin notificar **"]
    
    aux["Suma de Casos Acumulados"] = aux["Suma de Casos Acumulados"].apply(sacarPunto)
    aux["Suma de Casos Diarios"] = aux["Suma de Casos Diarios"].apply(sacarPunto)
    aux["Suma de Casos Activos"] = aux["Suma de Casos Activos"].apply(sacarPunto)
    aux["Suma de Recuperados"] = aux["Suma de Recuperados"].apply(sacarPunto)
    aux["Suma de Muertes"] = aux["Suma de Muertes"].apply(sacarPunto)
    return aux

def Validar():
    dataPDF = pd.read_html("https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/")
    diaActual = dateparser.parse(dataPDF[0][1][0].split("Chile")[1][1:])  #.strftime("%d-%m-%Y") 
    
    
    data = pd.read_excel("Archivo_original.xlsx")
    #data["Fecha Final"].max().strftime("%d-%m-%Y") == datetime.datetime.now().strftime("%d-%m-%Y")
    #print(data["Fecha Final"].max().strftime("%d-%m-%Y"))
    #if(data["Fecha Final"].max().strftime("%d-%m-%Y") != datetime.datetime.now().strftime("%d-%m-%Y")):     
    DataSalida = pd.read_excel("propios/Resumen_Regional.xlsx")

    if(data["Fecha Final"].max().strftime("%d-%m-%Y") != diaActual.strftime("%d-%m-%Y")):
        dataActual = calculoDeColumnas()
        DataSalida = pd.concat([data,dataActual])
     
    DataSalida.to_excel("propios/Resumen_Regional.xlsx", index=False)    
    DataSalida.to_csv("propios/Resumen_Regional.csv", index=False)      
    return DataSalida

def diaMes(fecha):
    mes = fecha.strftime("%m")
    switch = {
        "01":"ene",
        "02":"feb",
        "03":"mar",
        "04":"abr",
        "05":"may",
        "06":"jun",
        "07":"jul",
        "08":"ago",
        "09":"sep",
        "10":"oct",
        "11":"nov",
        "12":"dic"
    }
    salida = fecha.strftime("%d") + "-"+ switch.get(mes, "Error")
    return salida

def sacarPunto(numero):
    numero = str(numero)
    return int(numero.replace(".",""))

def calculoDeColumnas():
    dataPDF = pd.read_html("https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/")
    diaActual = dateparser.parse(dataPDF[0][1][0].split("Chile")[1][1:])
    data = Actualizar()
    dataOriginal = ArchivoOriginal()
    diaAnterior = (diaActual -  datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    dataDiaAnterior = dataOriginal[dataOriginal["FechaNumber"] == diaAnterior]
    dataDiaAnteriorLimpio = dataDiaAnterior[["Region","Suma de Muertes","Suma de Recuperados"]]
    dataDiaAnteriorLimpio.columns = ["Region","Muertes anterior","Recuperados anterior"]
    
    auxiliar = data.merge(dataDiaAnteriorLimpio, left_on="Region", right_on="Region", how='outer')
    auxiliar["Suma de Recuperados Diarios"] = auxiliar["Suma de Recuperados"] - auxiliar["Recuperados anterior"]
    del auxiliar["Recuperados anterior"]
    auxiliar["Suma de Fallecidos Diarios"] = auxiliar["Suma de Muertes"] - auxiliar["Muertes anterior"]
    del auxiliar["Muertes anterior"]
    
    return auxiliar

def ArreglarRegion(nombre):
    salida = nombre
    if("O'Higgins" == salida):
        salida = "O’Higgins"
    if("Araucania" == salida):
        salida = "Araucanía"
    return salida

def ResumenRegional2():
    filasInicial = len(pd.read_csv("propios/Resumen_Regional2.csv"))
    data = pd.read_csv("https://github.com/MinCiencia/Datos-COVID19/raw/master/output/producto3/TotalesPorRegion.csv")
    data = data.fillna(0)
    for categoria in data["Categoria"].unique():
        dataAux = data[data["Categoria"] == categoria]
        salida = []
        dataSinTotal = dataAux[dataAux["Region"] != "Total"]
        dataSoloTotal = dataAux[dataAux["Region"] == "Total"]
        for i in dataSinTotal.columns[2:]:
            #print(dataSinTotal[i].sum())
            diferencia = dataSoloTotal[i].iloc[0] -dataSinTotal[i].sum() 
            #print( diferencia)
            salida.append(diferencia)
        salida.insert(0,categoria)
        salida.insert(0,"No Informada")

        #lista.insert(0,0)
        data.loc[len(data)] = salida
    data = data[data["Region"] != "Total"]
    data["Region"] = data["Region"].apply(ArreglarRegion) 
    data = data.fillna(0)
    id_ = data.columns[:2].tolist()
    value = data.columns[2:].tolist()
    dataMelt = pd.melt(data, id_vars=id_, value_vars=value)
    columnas = ["Region","variable"]

    dataAux = dataMelt[dataMelt["Categoria"] == "Casos acumulados"]
    dataAux["Casos acumulados"] = dataAux["value"]
    del dataAux["value"]
    del dataAux["Categoria"]
    dataBase = dataAux   #dataBase.merge(dataAux,left_on=columnas, right_on=columnas, how='outer')

    for categoria in dataMelt["Categoria"].unique()[1:]:
        dataAux = dataMelt[dataMelt["Categoria"] == categoria]
        dataAux[categoria] = dataAux["value"]
        del dataAux["value"]
        del dataAux["Categoria"]
        dataBase = dataBase.merge(dataAux,left_on=columnas, right_on=columnas, how='outer')

    dataFinal = dataBase.fillna(0)


    salida = []
    for region in dataFinal["Region"].unique():
        dataAux = dataFinal[dataFinal["Region"] == region]
        
        lista = dataAux['Fallecidos totales'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        dataAux['FallecidosAux'] = lista
        dataAux["Casos nuevos fallecidos"] = dataAux["Fallecidos totales"] - dataAux["FallecidosAux"] 
        del dataAux["FallecidosAux"]
        
        lista = dataAux['Casos confirmados recuperados'].tolist()
        lista = lista[:-1]
        lista.insert(0,0)
        dataAux['RecuperadosAux'] = lista
        dataAux["Casos nuevos Recuperados"] = dataAux["Casos confirmados recuperados"] - dataAux["RecuperadosAux"] 
        del dataAux["RecuperadosAux"]
        salida.append(dataAux)
        
    DataSalida = pd.concat(salida)
    DataSalida["Fecha"] = DataSalida["variable"]
    del DataSalida["variable"]
    DataSalida.to_csv("propios/Resumen_Regional3.csv", index=False)
    DataSalida.to_excel("propios/Resumen_Regional3.xlsx", index=False) 
    del DataSalida["Casos confirmados por antigeno"]
    del DataSalida["Casos nuevos confirmados por antigeno"]
    del DataSalida["Casos con sospecha de reinfeccion"]
    print("PASAMOS POR AKA")
    print(DataSalida.columns)
    DataSalida.to_csv("propios/Resumen_Regional2.csv", index=False)
    DataSalida.to_excel("propios/Resumen_Regional2.xlsx", index=False) 
    filasFinal = len(pd.read_csv("propios/Resumen_Regional2.csv"))


    #if(filasInicial != filasFinal):
    #    print("Esperaremos 12 horas")
    #    time.sleep(43200)
    return DataSalida

def DescargarCSV(url,ruta):
    try:
        pd.read_csv(url).to_csv(ruta, index=False)
        print("Descarga desde " + url + " correcta")
    except:
        print("Error al descargar")    
    return



if __name__ == '__main__':
    print('Empezando proceso de descarga.')
    Ciclo()
    print('El roceso de descarga ha finalizado.')