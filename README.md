# Proyecto Integrador Parcial II - Secure CI/CD

Pipeline CI/CD seguro con modelo de mineria de datos (NO LLM) para clasificar codigo Java como seguro o vulnerable.

## Stack
- Java 17 + Spring Boot
- Python (scikit-learn) para el modelo ML
- GitHub Actions para CI/CD
- Railway para despliegue

## Dataset recomendado (publico)
- OWASP Benchmark y/o Juliet Test Suite (Java). Estos datasets cumplen con el requisito de ser publicos.

## Features minimas implementadas
- Tokens: conteo, unicidad, longitud promedio
- TF-IDF de tokens (uni/bi-gramas)
- AST depth (via javalang)
- Llamadas peligrosas (exec, ProcessBuilder, Statement.execute, etc.)
- Presencia de sanitizacion (PreparedStatement, escape, etc.)

## Estructura
- scripts/: extraccion de features, scoring y notificaciones
- ml/: modelo entrenado (`model.joblib`)
- notebooks/: notebook de entrenamiento
- .github/workflows/: pipelines

## Setup rapido
1) Crear ramas y protecciones
- Ramas obligatorias: `dev`, `test`, `main`
- Proteger `test` y `main` y exigir que el workflow de seguridad pase

2) Secrets en GitHub
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
dev
Nota: el despliegue se realiza via integracion GitHub de Railway (no requiere token).
=======
- `RAILWAY_TOKEN`
- `RAILWAY_SERVICE`
- `RAILWAY_PROJECT_ID`
test

3) Entrenar el modelo
- Abrir el notebook en [notebooks/train_model.ipynb](notebooks/train_model.ipynb)
- Descargar dataset (OWASP/Juliet) y convertir a CSV con columnas `code` y `label`
- Guardar el modelo final en `ml/model.joblib`

4) Pipeline
- Crear PR de `dev` -> `test`
- El pipeline ejecuta la clasificacion, pruebas y merges automaticos
- Al final, `main` dispara el despliegue en Railway por integracion GitHub

## Evidencias obligatorias (para el README final)
- Accuracy (CV) >= 82% con captura (actual: 0.873)
- Enlace a despliegue
- Capturas del bot de Telegram
- Notebook de entrenamiento

## PR de prueba
Este cambio es solo para activar el pipeline dev -> test.

## Notificaciones obligatorias cubiertas
- Inicio de revision de seguridad
- Resultado de clasificacion (probabilidad)
- Merge a test
- Resultado de pruebas
- Despliegue en produccion (exito/fallo)
- Rechazo por vulnerabilidad
