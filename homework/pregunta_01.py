"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    # Importar librerias
    import os
    import pandas as pd
    import warnings

    # Ignorar todas las advertencias
    warnings.filterwarnings("ignore")

    # Arreglar archivo txt colocando ';' en lugar de tabuladores (porque no lee los tabuladores)
    
    new_file = []

    with open('files/input/clusters_report.txt', "r", encoding="utf-8") as file:
        for line in (file):
            print(line)
            if len(line) > 15:
              if len(line) > 40:
                new_file.append(line[0:9] + ';' + line[9:25] + ';' + line[25:39] + ';' + line[39:])
              else:
                new_file.append(line[0:9] + ';' + line[9:25] + ';' + line[25:39] + ';' + "  ")
    
    if os.path.exists('files/input/new_clusters_report.txt'):
        os.remove('files/input/new_clusters_report.txt')    

    with open('files/input/new_clusters_report.txt', 'w', encoding='utf-8') as file:
        pass
    
    with open('files/input/new_clusters_report.txt', 'w', encoding='utf-8') as file:
        for line in new_file:
            file.write(line + '\n')

    # Leer archivo arreglado
    df = pd.read_csv('files/input/new_clusters_report.txt', sep=';', header=[0,1,2])
    print(df)
    print(df.columns)
    os.remove('files/input/new_clusters_report.txt') 

    # Ajustar nombres de columnas
    df.columns = df.columns.droplevel(2)
    nom_cols = []
    for campo in df.columns:
      nom_cols.append(campo[0].strip() + ' ' + campo[1].strip())
    df.columns = nom_cols
    print(df.columns)
    print(df)

    # Cambiar nombres de columnas
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    print(df.columns)

    # Rellenar registros del cluster
    df['cluster'] = df['cluster'].apply(lambda x: x.strip())
    etiqueta = df['cluster'][0]
    for i, element in enumerate(df['cluster']):
        if element != '':
            etiqueta = element
        else:
            df['cluster'][i] = etiqueta
    df['cluster'] = df['cluster'].apply(lambda x: int(x))
    print(df.cluster)

    # Agrupar por cluster
    df_grouped_1 = df.groupby('cluster').agg({'cantidad_de_palabras_clave': ' '.join})
    df_grouped_2 = df.groupby('cluster').agg({'porcentaje_de_palabras_clave': ' '.join})
    df_grouped_3 = df.groupby('cluster').agg({'principales_palabras_clave': ' '.join})

    # Unir dataframes
    df_agrupado = pd.merge(df_grouped_1, df_grouped_2, on='cluster')
    df_agrupado = pd.merge(df_agrupado, df_grouped_3, on='cluster')
    print(df_agrupado)

    # Ajustar registros de columna cantidad_de_palabras_clave
    df_agrupado['cantidad_de_palabras_clave'] = df_agrupado['cantidad_de_palabras_clave'].apply(lambda x: int(x.strip()))

    # Ajustar registros de columna porcentaje_de_palabras_clave
    df_agrupado['porcentaje_de_palabras_clave'] = df_agrupado['porcentaje_de_palabras_clave'].apply(lambda x: float(x.strip().replace(' %', '').replace(',', '.')))

    # Ajustar registros de columna principales_palabras_clave
    df_agrupado['principales_palabras_clave'] = df_agrupado['principales_palabras_clave'].apply(lambda x: x.split(', '))
    df = df_agrupado.reset_index()
    for i, lista in enumerate(df.principales_palabras_clave):
        cadena = ''
        for element in lista:
            element_l = element.split(' ')
            frase = ''
            for word in element_l:
                if word != '':
                    frase += word.strip() + ' '
            cadena += frase.strip() + ', '
        df.principales_palabras_clave[i] = cadena[:-2]
        if df.principales_palabras_clave[i][-1] == '.':
            df.principales_palabras_clave[i] = df.principales_palabras_clave[i][:-1]
 
    print(df)
    return df

pregunta_01()
