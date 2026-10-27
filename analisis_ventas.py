
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, regexp_replace, to_timestamp,
    upper, sum as spark_sum
)

# Crear sesion Spark
spark = SparkSession.builder \
    .appName("AnalisisVentasOnline") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Cargar datos originales
df = spark.read.csv(
    "/home/vboxuser/online_retail.csv",
    header=True,
    sep=";",
    encoding="UTF-8",
    inferSchema=False
)

print("\n=== DATOS ORIGINALES ===")
print("Total de registros:", df.count())

# Transformar tipos de datos
df_transformado = df \
    .withColumn(
        "Quantity",
        col("Quantity").cast("int")
    ) \
    .withColumn(
        "UnitPrice",
        regexp_replace(
            col("UnitPrice"), ",", "."
        ).cast("double")
    ) \
    .withColumn(
        "Fecha",
        to_timestamp(
            col("InvoiceDate"), "d/M/yyyy H:mm"
        )
    )

# Limpiar registros
df_limpio = df_transformado.filter(
    col("InvoiceNo").isNotNull() &
    (~upper(col("InvoiceNo")).startswith("C")) &
    col("Description").isNotNull() &
    (trim(col("Description")) != "") &
    col("Country").isNotNull() &
    (trim(col("Country")) != "") &
    (col("Quantity") > 0) &
    (col("UnitPrice") > 0) &
    col("Fecha").isNotNull()
)

# Calcular valor de cada linea de venta
df_limpio = df_limpio.withColumn(
    "TotalVenta",
    col("Quantity") * col("UnitPrice")
)

# Verificar resultados
print("\n=== RESULTADOS DE LIMPIEZA ===")

total_original = df.count()
total_limpio = df_limpio.count()

print("Registros originales:", total_original)
print("Registros limpios:", total_limpio)
print("Registros excluidos:",
      total_original - total_limpio)

print("\n=== DATOS TRANSFORMADOS ===")
df_limpio.select(
    "InvoiceNo", "Description", "Quantity",
    "UnitPrice", "Fecha", "TotalVenta"
).show(10, truncate=False)

print("\n=== INGRESOS TOTALES ===")
df_limpio.agg(
    spark_sum("TotalVenta").alias("IngresosTotales")
).show()



# ANALISIS EXPLORATORIO DE DATOS (EDA)


from pyspark.sql.functions import (
    desc, year, month, countDistinct,
    round as spark_round
)

# 1. Los 10 productos mas vendidos
print("\n=== TOP 10 PRODUCTOS MAS VENDIDOS ===")

productos = df_limpio.groupBy("Description") \
    .agg(
        spark_sum("Quantity").alias("UnidadesVendidas"),
        spark_round(
            spark_sum("TotalVenta"), 2
        ).alias("Ingresos")
    ) \
    .orderBy(desc("UnidadesVendidas")) \
    .limit(10)

productos.show(10, truncate=False)


# 2. Los 10 paises con mayores ingresos
print("\n=== TOP 10 PAISES POR INGRESOS ===")

paises = df_limpio.groupBy("Country") \
    .agg(
        spark_round(
            spark_sum("TotalVenta"), 2
        ).alias("Ingresos"),
        countDistinct("InvoiceNo").alias("Facturas")
    ) \
    .orderBy(desc("Ingresos")) \
    .limit(10)

paises.show(10, truncate=False)


# 3. Evolucion de las ventas mensuales
print("\n=== VENTAS POR MES ===")

ventas_mensuales = df_limpio \
    .withColumn("Anio", year("Fecha")) \
    .withColumn("Mes", month("Fecha")) \
    .groupBy("Anio", "Mes") \
    .agg(
        spark_round(
            spark_sum("TotalVenta"), 2
        ).alias("Ingresos")
    ) \
    .orderBy("Anio", "Mes")

ventas_mensuales.show(20, truncate=False)


# 4. Guardar resultados para las graficas
print("\n=== EXPORTANDO RESULTADOS ===")

productos.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("/home/vboxuser/resultados_productos")

paises.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("/home/vboxuser/resultados_paises")

ventas_mensuales.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("/home/vboxuser/resultados_mensuales")

print("Resultados exportados correctamente")

spark.stop()

