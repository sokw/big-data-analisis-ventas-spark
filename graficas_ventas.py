
import os
import glob
import csv
import matplotlib

# Guardar imagenes sin entorno grafico
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/home/vboxuser"
SALIDA = os.path.join(BASE, "graficas_ventas")

os.makedirs(SALIDA, exist_ok=True)

# Leer los resultados exportados por Spark
def leer_resultados(carpeta):
    archivos = glob.glob(
        os.path.join(BASE, carpeta, "part-*.csv")
    )

    if not archivos:
        raise FileNotFoundError(
            f"No se encontro el CSV en {carpeta}"
        )

    with open(archivos[0], "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


productos = leer_resultados("resultados_productos")
paises = leer_resultados("resultados_paises")
mensuales = leer_resultados("resultados_mensuales")

# GRAFICA 1: Productos mas vendidos
nombres = [x["Description"] for x in productos]
cantidades = [int(x["UnidadesVendidas"]) for x in productos]

fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(nombres[::-1], cantidades[::-1], color="#2563eb")
ax.set_title("Los 10 productos mas vendidos")
ax.set_xlabel("Unidades vendidas")
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(
    os.path.join(SALIDA, "productos_mas_vendidos.png"),
    dpi=180, bbox_inches="tight"
)
plt.close(fig)

# GRAFICA 2: Ingresos por pais
nombres = [x["Country"] for x in paises]
ingresos = [float(x["Ingresos"]) for x in paises]

fig, ax = plt.subplots(figsize=(11, 6))
ax.bar(nombres, ingresos, color="#0d9488")
ax.set_title("Ingresos por pais")
ax.set_ylabel("Ingresos en libras esterlinas (GBP)")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(
    os.path.join(SALIDA, "ingresos_por_pais.png"),
    dpi=180, bbox_inches="tight"
)
plt.close(fig)

# GRAFICA 3: Ventas mensuales
periodos = [
    f'{x["Anio"]}-{int(x["Mes"]):02d}'
    for x in mensuales
]
valores = [float(x["Ingresos"]) for x in mensuales]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(periodos, valores, marker="o",
        color="#7c3aed", linewidth=2)
ax.set_title("Evolucion mensual de los ingresos")
ax.set_xlabel("Mes")
ax.set_ylabel("Ingresos en libras esterlinas (GBP)")
ax.tick_params(axis="x", rotation=45)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(
    os.path.join(SALIDA, "ventas_mensuales.png"),
    dpi=180, bbox_inches="tight"
)
plt.close(fig)

print("\nGRAFICAS GENERADAS CORRECTAMENTE")
print("Ubicacion:", SALIDA)
for archivo in os.listdir(SALIDA):
    print("-", archivo)
