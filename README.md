Análisis de ventas con Apache Spark y Python

Proyecto académico – Big Data, Tarea 3

Universidad: Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Big Data
Código: 202016911
Actividad: Tarea 3 – Procesamiento de Datos con Apache Spark

1. Descripción del proyecto

Este proyecto desarrolla un análisis de ventas de una tienda virtual mediante Apache Spark y Python, utilizando técnicas de procesamiento de datos por lotes (batch).

Se trabaja con el conjunto de datos Online Retail, que contiene 541.909 registros de transacciones comerciales realizadas entre diciembre de 2010 y diciembre de 2011.

El objetivo es identificar los productos con mayores cantidades vendidas, los países que generan mayores ingresos y la evolución mensual de las ventas.

2. Herramientas utilizadas

Ubuntu Linux en VirtualBox.

Apache Spark y PySpark.

Python.

Matplotlib para la generación de gráficas.

Archivos CSV para el almacenamiento y procesamiento de datos.

3. Conjunto de datos

Nombre: Online Retail
Fuente: UCI Machine Learning Repository
Autor del conjunto de datos: Daqing Chen (2015)

Enlace: https://archive.ics.uci.edu/dataset/352/online+retail

El archivo original está disponible en Excel y fue convertido a CSV para facilitar su lectura con Apache Spark.

El CSV utilizado emplea punto y coma como separador de columnas y coma como separador decimal.

4. Procesamiento de datos

El procesamiento se desarrolla mediante el programa analisis_ventas.py, que realiza las siguientes operaciones:

Carga del conjunto de datos utilizando PySpark.

Exploración de la estructura y cantidad de registros.

Conversión de cantidades, precios y fechas.

Filtrado de cancelaciones, valores no positivos y registros que no cumplen los criterios de limpieza.

Cálculo de ingresos mediante cantidad multiplicada por precio.

Identificación de los diez productos más vendidos.

Cálculo de ingresos por país.

Análisis de la evolución mensual de las ventas.

Exportación de los resultados a archivos CSV.

5. Resultados obtenidos

Indicador                                                           Resultado

Registros originales                                                541.909

Registros después de limpieza                                        530.104

Registros excluidos                                                 11.805

Ingresos aproximados analizados                                     £10.666.684,54

Producto con más unidades vendidas                                   PAPER CRAFT, LITTLE BIRDIE

Unidades del producto principal                                      80.995

País con mayores ingresos                                            Reino Unido

Mes con mayores ingresos                                             Noviembre de 2011

Los resultados corresponden a ventas positivas después de aplicar los filtros definidos. No representan necesariamente las ventas netas, porque las cancelaciones y devoluciones fueron excluidas del análisis.

6. Visualización de resultados

El programa graficas_ventas.py permite generar tres visualizaciones:

productos_mas_vendidos.png: los diez productos con mayores cantidades vendidas.

ingresos_por_pais.png: comparación de los ingresos entre países.

ventas_mensuales.png: evolución de los ingresos mensuales.

Estas gráficas se generan a partir de los resultados exportados mediante Apache Spark.

7. Instrucciones de ejecución

Requisitos

Disponer de Python, Apache Spark con PySpark y Matplotlib.

Preparación

Descargar el conjunto de datos Online Retail desde UCI Machine Learning Repository.

Convertir el archivo Excel a CSV.

Copiar el archivo a Ubuntu con el nombre online_retail.csv.

Ubicar el archivo en /home/vboxuser/online_retail.csv, o modificar esa ruta en analisis_ventas.py según el entorno de ejecución.

Ejecutar el procesamiento batch

Desde la terminal de Ubuntu:

spark-submit analisis_ventas.py

Este comando carga, limpia, transforma y analiza los datos, y genera tres directorios de resultados:

/home/vboxuser/resultados_productos

/home/vboxuser/resultados_paises

/home/vboxuser/resultados_mensuales

Generar las gráficas

Ejecutar:

python3 graficas_ventas.py

El programa genera las imágenes en:

/home/vboxuser/graficas_ventas/

Los programas emplean rutas absolutas de la máquina virtual utilizada durante la práctica. Para ejecutarlos en otro equipo es necesario ajustar esas rutas.

8. Conclusión

El desarrollo del proyecto permitió aplicar Apache Spark al procesamiento distribuido de un conjunto de datos comerciales, realizando operaciones de carga, limpieza, transformación y análisis exploratorio.

Los resultados permitieron identificar productos destacados, mercados relevantes y variaciones mensuales en los ingresos, demostrando la utilidad de PySpark para procesar y analizar información.
