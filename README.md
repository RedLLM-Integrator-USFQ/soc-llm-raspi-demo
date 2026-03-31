# Documentación MVP: Primer Sprint CapacitaSOC

## Historias de Usuario Épicas

**Épica 1:** Como equipo de desarrollo, queremos establecer el entorno de gestión del proyecto y preparar la infraestructura principal, para tener una base controlada donde desplegar nuestros servicios.

**Épica 2:** Como equipo de backend y datos, queremos levantar las bases vectoriales y los motores de IA dentro de contenedores, para validar que el hardware soporta las tecnologías elegidas.

**Épica 3:** Como equipo de frontend, queremos construir la estructura inicial del dashboard en un entorno aislado, para garantizar el desarrollo visual sin conflictos de dependencias.

## Issues por Roles

### Felipe, SecOps y Scrum Master / Project Manager

#### Issue 1: Configurar repositorio oficial y tablero Kanban

**Historia de Usuario:** Épica 1

**Descripción:** Necesitamos establecer el entorno de gestión oficial del proyecto usando GitHub Projects. El objetivo es dar una descripción por encima de todo de las tareas iniciales y revisar si es que funcionó el flujo de trabajo para todos los integrantes.

**Criterios de Aceptación:** Repositorio oficial creado y tablero Kanban activo con las columnas listas.

**Label:** scrum-master

#### Issue 2: Instalar motor de contenedores en Nodo 1

**Historia de Usuario:** Épica 1

**Descripción:** Hay que preparar la Raspberry Pi principal instalando Docker para tener la base controlada donde desplegaremos los servicios. El objetivo es dar una descripción por encima de todo del proceso de instalación y revisar si es que funcionó levantando un contenedor básico de prueba.

**Criterios de Aceptación:** Docker instalado en el Nodo 1 y contenedor de prueba ejecutándose sin errores en la consola.

**Label:** secops

### Vai, Frontend

#### Issue 3: Crear y dockerizar proyecto base para el dashboard

**Historia de Usuario:** Épica 3

**Descripción:** Se debe construir la estructura inicial de la aplicación web y empaquetarla en un Dockerfile. El objetivo es dar una descripción por encima de todo de la vista inicial y revisar si es que funcionó al abrirlo en el navegador local.

**Criterios de Aceptación:** Proyecto base inicializado, Dockerfile configurado y contenedor levantado cargando la pantalla de inicio.

**Label:** frontend

### Alejo, DevOps, API y AI/ML

#### Issue 4: Estructurar servidor base en FastAPI

**Historia de Usuario:** Épica 2

**Descripción:** Necesitamos armar la API inicial que recibirá las peticiones del frontend usando Python y FastAPI dentro de un contenedor Docker. El objetivo es dar una descripción por encima de todo de las rutas base y revisar si es que funcionó haciendo una petición simple de prueba.

**Criterios de Aceptación:** Archivo principal configurado, Dockerfile creado y API respondiendo correctamente.

**Label:** devops-api

#### Issue 5: Ejecutar y evaluar motor de IA en Nodo 2

**Historia de Usuario:** Épica 2

**Descripción:** Hay que levantar el motor cognitivo en la segunda Raspberry Pi para descargarle peso computacional al Nodo 1. Además, se debe probar y testear qué modelo de lenguaje es más capaz o estable para integrarlo en la arquitectura final del proyecto. El objetivo es dar una descripción por encima de todo del rendimiento de memoria, comparar un par de opciones y revisar si es que funcionó la ejecución del modelo ganador de forma local.

**Criterios de Aceptación:** Docker instalado en el Nodo 2, imagen oficial de Ollama corriendo exitosamente y pruebas de rendimiento realizadas con al menos dos modelos diferentes para elegir el definitivo.

**Label:** ai-ml

### Bri y Dani, Backend y Data

#### Issue 6: Configurar base vectorial Qdrant

**Historia de Usuario:** Épica 2

**Descripción:** Se debe preparar el almacenamiento de memoria vectorial para el sistema RAG usando la imagen oficial de Qdrant en Docker. El objetivo es dar una descripción por encima de todo de la conexión y revisar si es que funcionó abriendo el puerto de la base de datos sin errores de rechazo.

**Criterios de Aceptación:** Archivo de configuración listo, contenedor en ejecución y puerto respondiendo a conexiones.

**Label:** backend-data

**Assignee:** Bri

#### Issue 7: Crear entorno aislado de Python para procesamiento

**Historia de Usuario:** Épica 2

**Descripción:** Necesitamos un entorno limpio para escribir los filtros de texto y procesar los logs de seguridad en el futuro mediante un Dockerfile con sus librerías base. El objetivo es dar una descripción por encima de todo de las dependencias necesarias y revisar si es que funcionó manteniendo el contenedor encendido y estable.

**Criterios de Aceptación:** Archivo de requerimientos creado, Dockerfile configurado y contenedor ejecutándose de forma estable.

**Label:** backend-data

**Assignee:** Dani

### Ahmed, Solutions Architect y QA

#### Issue 8: Diseñar y complementar propuesta de Arquitectura V2

**Historia de Usuario:** Épica 1

**Descripción:** Hay que complementar la arquitectura propuesta actualmente y diseñar la segunda versión formal adaptada específicamente para la migración al servidor NVIDIA DGX Spark. Se debe incluir la investigación sobre herramientas de gating y memoria vectorial para casos previos. El objetivo es dar una descripción por encima de todo de esta nueva topología y revisar si es que funcionó la propuesta al presentarla con el equipo.

**Criterios de Aceptación:** Documento maestro en la nube creado, diagrama inicial de la V2 estructurado y secciones de investigación redactadas.

**Label:** solutions-architect
