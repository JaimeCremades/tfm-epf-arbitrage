# Electricity Price Forecasting and Battery Arbitrage
### TFM — Máster Universitario en Ciencia de Datos e Inteligencia Artificial
### CUNEF Universidad | Jaime Cremades Castelló | 2026

## Descripción

Este repositorio contiene el código completo del Trabajo de Fin de Máster sobre predicción de precios eléctricos en el mercado mayorista español (OMIE) y su aplicación a estrategias de arbitraje energético con batería normalizada de 1 MWh.

Se implementan y comparan siete modelos de predicción pertenecientes a cuatro familias metodológicas: estadística, machine learning, redes neuronales y modelos probabilísticos. Las predicciones se evalúan tanto en términos de error estadístico (MAE, RMSE, MAPE, sMAPE) como de beneficio económico de arbitraje.

## Modelos implementados

| Modelo | Familia | MAE (EUR/MWh) | Eficiencia arbitraje |
|---|---|---|---|
| SARIMA | Estadístico | 19.89 | 88.0% |
| XGBoost | Machine Learning | 7.72 | 91.7% |
| LSTM | Red neuronal recurrente | 33.14 | 77.1% |
| N-BEATS | Red de expansión de bases | 28.89 | 86.1% |
| NBEATSx | N-BEATS multivariante | 9.80 | 79.4% |
| BiGRU-KAN | Red híbrida recurrente-KAN | 31.23 | 80.9% |
| BNN con MC Dropout | Red bayesiana probabilística | 12.62 | 90.1% |

## Estructura del repositorio
```
├── 01_pipeline_datos.ipynb         # Descarga y preprocesamiento del dataset
├── 02_eda.ipynb                    # Análisis exploratorio de datos
├── 03_modelos.ipynb                # Entrenamiento y evaluación de modelos
├── 04_arbitraje.ipynb              # Estrategia de arbitraje energético
├── 05_comparaciones.ipynb          # Unificación de predicciones
└── README.md
```
## Dataset

El dataset cubre el periodo enero 2020 — febrero 2026 con frecuencia horaria. Las fuentes de datos son:

- **OMIE** — precio horario del mercado mayorista español
- **REE/ESIOS** — demanda, generación por tecnología y variables previstas PBF
- **Open-Meteo** — temperatura y velocidad del viento previstas
- **Investing.com** — precio del gas natural TTF y CO₂

El dataset final contiene 26 variables y 54.072 registros horarios.

## Requisitos

```bash
pip install pandas numpy matplotlib scikit-learn xgboost torch statsmodels neuralforecast scipy
```

## Uso

Los notebooks están numerados en orden de ejecución. Se recomienda ejecutar en Google Colab Pro con GPU A100.

## Referencia

Si utilizas este código, por favor cita:

> Cremades Castelló, J. (2026). *Estimación de precios de la electricidad y arbitraje energético con batería mediante modelos de machine learning y redes neuronales*. Trabajo de Fin de Máster, CUNEF Universidad.