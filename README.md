# EcoTech Solutions — Evaluación 3

**Asignatura:** Programación Orientada a Objeto Seguro  
**Carrera:** Ingeniería en Ciberseguridad — INACAP

## Descripción del proyecto

EcoTech Solutions es un sistema desarrollado en Python que permite gestionar empleados, departamentos, proyectos y registros de horas de trabajo.

En esta tercera evaluación continué mejorando el proyecto de las unidades anteriores, agregando nuevas funciones relacionadas con la seguridad, el inicio de sesión, las consultas a servicios externos y el almacenamiento de información en SQLite.

La idea principal fue mantener el sistema que ya tenía y hacerlo más completo, considerando las necesidades de la empresa y los contenidos vistos en clases.

## Funcionalidades principales

El sistema cuenta con dos tipos de usuarios: administrador y empleado.

**Administrador**

Puede acceder a las funciones de gestión de empleados, departamentos, proyectos, registros de tiempo, usuarios y permisos. También puede registrar cuentas de empleados y utilizar los servicios externos.

**Empleado**

Puede consultar su información personal, modificar los datos permitidos, revisar sus registros de tiempo y acceder a los servicios externos, sin tener permisos para administrar información de otros empleados.

## Servicios externos

Se incorporaron dos servicios que permiten obtener información desde internet mediante APIs.

### Consulta del dólar

El sistema consulta el valor del dólar desde la API de mindicador.cl.

Permite:

- Consultar el valor del dólar y verificar su fecha.
- Guardar cotizaciones en SQLite.
- Revisar el historial de cotizaciones.
- Convertir presupuestos de pesos chilenos a dólares.

Cada vez que se utiliza la consulta, el programa solicita información actualizada. Si el servicio entrega una cotización de una fecha anterior, se informa al usuario para evitar utilizarla como si fuera del día actual.

### Consulta del clima

El sistema utiliza Open-Meteo para consultar las condiciones climáticas de cuatro ciudades de Chile:

1. Antofagasta
2. Santiago
3. Coquimbo
4. Concepción

El usuario selecciona una ciudad mediante un menú y el programa muestra información como la temperatura, humedad, estado del tiempo y fecha de la medición.

Esta función permite considerar las condiciones climáticas al momento de planificar actividades o proyectos.

## Seguridad y validaciones

Para mejorar la seguridad del sistema se implementaron distintas medidas:

- Inicio de sesión mediante usuario y contraseña.
- Contraseñas almacenadas mediante hash con sal.
- Permisos diferenciados entre administrador y empleado.
- Validación de datos ingresados por el usuario.
- Control de registros duplicados.
- Uso de `try` y `except` para manejar errores.
- Control de errores de conexión con servicios externos.

También se mejoró el registro de cuentas. Si el usuario se equivoca al confirmar su contraseña, solamente debe repetir la confirmación, sin comenzar nuevamente todo el proceso.

## Base de datos y semillas

Se utiliza SQLite para almacenar la información del sistema.

El proyecto incluye semillas de datos para crear registros de ejemplo de empleados, departamentos, proyectos, registros de tiempo, cuentas de usuario y relaciones entre entidades.

Las fechas de los datos de ejemplo se calculan al momento de ejecutar las semillas, tomando como referencia la fecha actual de Chile.

Las cotizaciones reales del dólar no se generan mediante semillas, ya que deben obtenerse desde el servicio externo.

## Instalación y ejecución

Primero se deben instalar las dependencias desde la carpeta principal del proyecto:

```bash
python -m pip install -r requirements.txt
```

En Windows, si aparece un error relacionado con la zona horaria `America/Santiago`, se debe instalar:

```bash
python -m pip install tzdata
```

Para iniciar el programa:

```bash
python src/main.py
```

Para cargar las semillas de datos:

```bash
python src/semilla_bd.py
```

Es recomendable respaldar el archivo `ecotech.db` antes de reemplazar el proyecto o cargar información nueva.

## Organización del proyecto

- `src/main.py`: inicio del programa, autenticación y menú principal.
- `src/dominio/`: clases y validaciones.
- `src/menus/`: menús de las diferentes funcionalidades.
- `src/servicios/`: autenticación, consultas del dólar y clima.
- `src/persistencia/`: conexión y operaciones con la base de datos.
- `src/semilla_bd.py`: generación de datos de ejemplo.
- `Docs/`: diagramas UML del sistema.
- `integracion_IA.md`: explicación del apoyo de inteligencia artificial durante el desarrollo.

## Relación con la Evaluación 3

El proyecto aborda los cuatro aspectos principales solicitados en la guía:

1. **Consumo de APIs:** consultas del dólar y clima mediante solicitudes HTTP y procesamiento de JSON.
2. **Seguridad:** autenticación, protección de contraseñas, validaciones y control de permisos.
3. **Manejo de errores:** utilización de excepciones para controlar entradas incorrectas y fallas externas.
4. **Uso crítico de IA:** apoyo para revisar, corregir y mejorar el código, documentando los cambios realizados.

## Conclusión

Durante esta evaluación aprendí a conectar un programa de Python con servicios externos, trabajar con respuestas JSON y guardar información en SQLite. También pude entender mejor la importancia de validar los datos, proteger las contraseñas y controlar los errores para que el programa funcione de manera más segura.

Lo que más me ayudó fue ir probando las funciones y corrigiendo los problemas que aparecían, porque así pude comprender mejor cómo funciona cada parte del proyecto.