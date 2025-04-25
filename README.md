# 🎈 Sistema de pronóstico de ventas semanales

Aplicación interactiva para el análisis y pronóstico de ventas semanales en tiendas minoristas de EE.UU. Utiliza modelos de machine learning para generar proyecciones basadas en datos históricos del período 2010–2012.

🔗 **Puedes ver la app funcionando aquí**:  
[![Open in Streamlit](https://ventasusa2012.streamlit.app)](https://ventasusa2012.streamlit.app)

---

## ℹ️ Información del proyecto

Este sistema está diseñado para explorar y predecir el comportamiento de ventas semanales en 45 tiendas distribuidas por Estados Unidos. A partir de un conjunto de datos históricos, la plataforma permite visualizar patrones de venta y generar proyecciones utilizando modelos de regresión avanzados implementados en Python:

- `RandomForestRegressor`
- `GradientBoostingRegressor`
- `XGBRegressor`

### 🧭 Funcionalidades principales

- **Series por tienda**: Visualización temporal de variables clave para cada tienda.
- **Ventas totales por ciudad**: Análisis agregado de ventas con visualización geográfica y comparativa.
- **Análisis temporal**: Evaluación de patrones anuales y mensuales de ventas por tienda y ciudad.
- **Modelado predictivo**: Comparación visual entre valores reales y predichos por distintos modelos.
- **Forecasting**: Herramienta interactiva para generar predicciones de ventas futuras en un rango de fechas seleccionado.

---

## ⚙️ Cómo ejecutarlo localmente

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
2. jecuta la aplicación:
   ``` bash
   streamlit run streamlit_app.py
