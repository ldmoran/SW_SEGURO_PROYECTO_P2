# Universidad de las Fuerzas Armadas ESPE

## Departamento de Ciencias de la Computaci ́on

```
Carrera de Ingenier ́ıa en Software
```
```
Desarrollo de Software Seguro
```
# Proyecto Integrador Parcial II

## Profesor: Geovanny Cudco

## 28 de mayo de 2026

# 1. Tema

Desarrollo e Implementaci ́on de un Pipeline CI/CD Seguro con integraci ́on de IA para
la Detecci ́on Autom ́atica de Vulnerabilidades en c ́odigo fuente mediante un Modelo de
Miner ́ıa de Datos.

# 2. Tipo de actividad

```
Proyecto pr ́actico individual o en equipo (m ́aximo 3 personas).
```
# 3. Objetivo

Dise ̃nar, implementar y demostrar un pipeline CI/CD completamente automatizado
y seguro que integre un modelo de inteligencia artificial basado en t ́ecnicas de miner ́ıa
de datos capaz de clasificar c ́odigo fuente como seguro o vulnerable, permitiendo que
́unicamente el c ́odigo considerado seguro llegue a producci ́on, garantizando as ́ı la aplicaci ́on
de los principios de Secure DevOps y Shift-Left Security.
IMPORTANTE: Est ́a estrictamente prohibido la incorporaci ́on de tecnolog ́ıas de
Large Language Models (LLM) como GPT, Claude, Llama, CodeLlama, etc. El modelo de
IA debe ser obligatoriamente un clasificador de miner ́ıa de datos tradicional (scikit-learn,
XGBoost, Random Forest, SVM, etc.) entrenado por Ud, usando datasets p ́ublicos (o
propios) de c ́odigo vulnerable/seguro.


# 4. Descripci ́on

El proyecto consiste en crear una infraestructura CI/CD segura y automatizada que
procese c ́odigo fuente presentado por un usuario en una rama de testing de un repositorio
Git (usando GitHub o GitLab). El flujo debe ser el siguiente:

## 4.1. Flujo de trabajo requerido

4.1.1. Ramas obligatorias

```
dev→ rama de desarrollo (donde el desarrollador hace push)
```
```
test→ rama de staging /pruebas
```
```
main→ rama de producci ́on
```
4.1.2. Trigger

```
El pipeline se activa autom ́aticamente al crear un Pull Request de dev→ test.
```
4.1.3. Etapas del Pipeline (todas obligatorias y automatizadas)

```
Etapa 1: Revisi ́on de Seguridad con Modelo de Miner ́ıa de Datos
```
```
Se ejecuta un job que descarga el diff del PR.
Se procesa el c ́odigo modificado (extrayendo features como tokens,
AST simplificado, patrones de llamadas a funciones peligrosas, uso de
sanitizaci ́on, etc.).
Se clasifica el c ́odigo como SEGURO o VULNERABLE utilizando
exclusivamente un modelo de machine learning cl ́asico (scikit-learn,
XGBoost, etc.).
Si el modelo devuelve ”VULNERABLE”:
```
- El PR se marca autom ́aticamente como rejected.ose bloquea el
    merge.
- Se crea un comentario detallado en el PR con la probabilidad y
    tipo de vulnerabilidad detectada.
- Se env ́ıa notificaci ́on inmediata v ́ıa Telegram al desarrollador con
    el detalle.
- Se aplica la etiqueta ”fixing-required^2 se crea una issue autom ́atica
    vinculada.
Si el modelo devuelve ”SEGURO”→ contin ́ua el pipeline.

```
Etapa 2: Merge Autom ́atico a rama test + Pruebas
```
```
Merge autom ́atico a test.
Ejecuci ́on de pruebas unitarias e integraci ́on (pytest, Jest, JUnit, etc.).
Si alguna prueba falla → bloqueo y notificaci ́on Telegram + etiqueta
“tests-failed”.
```

```
Etapa 3: Merge a main y Despliegue en Producci ́on
```
```
Solo si todo lo anterior pas ́o → merge autom ́atico a main.
Build de imagen Docker y despliegue autom ́atico en un proveedor
gratuito:
```
- Opciones permitidas: Render, Railway, Fly.io, Vercel (para frontend),
    Northflank, o Docker Hub + Play with Docker (para demo).
- Tambi ́en permitido: Heroku (si a ́un tiene plan gratuito disponible).
- Otro que considere el estudiante.
Notificaci ́on final de ́exito v ́ıa Telegram y/o email.

4.1.4. Notificaciones obligatorias en todas las fases:

Deben enviarse mensajes v ́ıa Telegram (bot propio) o correo electr ́onico en los siguientes
eventos:

```
Inicio de revisi ́on de seguridad
```
```
Resultado de la clasificaci ́on del modelo (seguro/vulnerable + probabilidad)
```
```
Merge a test realizado
```
```
Resultado de pruebas
```
```
Despliegue en producci ́on exitoso o fallido
```
```
Rechazo por vulnerabilidad (con detalle)
```
# 5. Requisitos

```
a. Modelo de miner ́ıa de datos entrenado por el estudiante (deben entregar el .pkl o
.joblib).
```
```
b. Dataset utilizado debe ser p ́ublico (recomendados: kaggle, Big-Vul, DiverseVul,
CVEFixes, o synthetic con Juliet Test Suite).
```
```
c. Features m ́ınimas: tokens, AST depth, llamadas a funciones peligrosas (eval, exec,
subprocess, SQL raw, etc.), presencia de sanitizaci ́on/escapes.
```
```
d. Accuracy m ́ınima demostrada: 82 % en validaci ́on cruzada (deben mostrarlo en el
README).
```
```
e. Telegram Bot propio (token en GitHub Secrets).
```
```
f. Despliegue real y funcional (debe estar online y accesible).
```
```
g. Branch protection rules activadas en test y main (requerir revisi ́on de seguridad
aprobada).
```

# 6. Formato de entrega

```
a. Repositorio GitHub o GitLab p ́ublico o con acceso otorgado al profesor.
```
```
b. README.md completo con::
```
```
Instrucciones de setup del pipeline
C ́omo entrenaron el modelo (notebook incluido)
Capturas y enlace al bot de Telegram
Enlace al despliegue en producci ́on
```
```
c. Informe t ́ecnico en Latex se adjunta el formato del informe.
```
```
d. Exposici ́on de 8-12 minutos mostrando:
```
```
C ́odigo vulnerable → rechazo autom ́atico
C ́odigo seguro → flujo completo hasta producci ́on
```
# 7. Fecha de entrega

```
Fecha de Entrega: 18 de junio de 2026, 23:59 horas.
```
Nota importante:
Bajo ning ́un concepto se recibir ́an actividades fuera del plazo establecido. No se
otorgar ́an pr ́orrogas individuales ni se aceptar ́an entregas tard ́ıas por ning ́un medio.
Es responsabilidad del estudiante gestionar oportunamente su trabajo y asegurar el
cumplimiento del cronograma.

# 8. Criterios de Evaluaci ́on

```
a. Funcionalidad completa del pipeline (automatizaci ́on total): 6 puntos
```
```
b. Modelo de miner ́ıa de datos propio y efectivo (prohibido LLM): 6 puntos
```
```
c. Notificaciones Telegram/correo electr ́onico en todas las fases + issues autom ́aticas:
3 puntos
```
```
d. Despliegue autom ́atico en proveedor gratuito y funcional: 3 puntos
```
```
e. Calidad del informe y documentaci ́on (README + notebook): 2 puntos
```
```
Penalizaciones
```
```
a. Uso de LLM (incluso parcial): 20 puntos (nota 0 autom ́atico)
```
```
b. Pipeline no completamente autom ́atico: 4 a 6 puntos
```
```
c. Sin despliegue real: 3 puntos
```
```
d. Otras.
```

