# Sistema Web de Detección de Billetes

## Descripción del proyecto

Este proyecto consiste en el desarrollo de una aplicación web que permite realizar el reconocimiento y análisis de billetes mediante el procesamiento de imágenes. Su objetivo es facilitar la identificación de billetes a través de una plataforma sencilla, donde el usuario pueda cargar una imagen para que el sistema la analice y muestre los resultados correspondientes.

La aplicación busca aprovechar herramientas de programación y procesamiento digital de imágenes para ofrecer una alternativa tecnológica que facilite este proceso.

## Objetivo general

Desarrollar una aplicación web capaz de analizar imágenes de billetes mediante técnicas de procesamiento digital de imágenes, proporcionando al usuario información sobre el resultado del reconocimiento.

## Tecnologías utilizadas

Las principales herramientas y tecnologías utilizadas en el desarrollo del proyecto son:

- **Python:** lenguaje de programación utilizado para desarrollar la lógica del sistema.
- **Django:** framework utilizado para construir la aplicación web y gestionar sus funcionalidades.
- **HTML:** utilizado para estructurar las páginas de la aplicación.
- **CSS:** encargado del diseño y presentación visual de la interfaz.
- **JavaScript:** utilizado para agregar interactividad en la aplicación.
- **OpenCV:** biblioteca utilizada para el procesamiento y análisis de imágenes.
- **NumPy:** herramienta utilizada para realizar operaciones y cálculos relacionados con el procesamiento de imágenes.
- **SQLite:** sistema de base de datos utilizado durante el desarrollo.
- **Git y GitHub:** utilizados para el control de versiones y almacenamiento del código fuente.

## Funcionalidades principales

- Acceso a la aplicación mediante una interfaz web.
- Carga de imágenes de billetes.
- Procesamiento de imágenes mediante herramientas de visión artificial.
- Análisis de las características visuales de las imágenes.
- Presentación de resultados al usuario.
- Organización de las funcionalidades mediante Django.

## Estructura del proyecto

La organización principal del proyecto es la siguiente:

```text
billetes-project/
│
├── detector/
│   └── Aplicación principal para la detección de billetes
│
├── mysite/
│   └── Configuración general del proyecto Django
│
├── media/
│   └── Archivos e imágenes cargadas
│
├── staticfiles/
│   └── Archivos estáticos de la aplicación
│
├── manage.py
│   └── Archivo para administrar el proyecto Django
│
├── requirements.txt
│   └── Dependencias necesarias para ejecutar el proyecto
│
├── .gitignore
│   └── Archivos excluidos del control de versiones
│
└── README.md
    └── Documentación del proyecto
```

## Instalación y ejecución

Para ejecutar el proyecto de manera local, es necesario contar con Python instalado.

**1. Clonar el repositorio**

```bash
git clone URL_DEL_REPOSITORIO
```

**2. Entrar a la carpeta del proyecto**

```bash
cd billetes-project
```

**3. Crear un entorno virtual**

```bash
py -m venv .venv
```

**4. Activar el entorno virtual en Windows**

```powershell
.venv\Scripts\Activate.ps1
```

**5. Instalar las dependencias**

```bash
py -m pip install -r requirements.txt
```

**6. Realizar las migraciones**

```bash
py manage.py migrate
```

**7. Ejecutar el servidor**

```bash
py manage.py runserver
```

**8. Abrir la aplicación**

En el navegador, ingresar a:

https://billetes-project.onrender.com 

## Desarrollo del proyecto

El sistema se desarrolla utilizando Django como framework principal. La aplicación se encarga de recibir las imágenes proporcionadas por el usuario y procesarlas mediante bibliotecas especializadas como OpenCV y NumPy.

El proyecto se encuentra organizado en diferentes archivos y módulos para facilitar su mantenimiento, modificación y crecimiento en futuras etapas.

## Estado actual del proyecto

El proyecto se encuentra en desarrollo. Se trabaja en la integración de las funcionalidades de procesamiento de imágenes, la interfaz de usuario y la comunicación entre los diferentes componentes de la aplicación.

## Autores
Gonzalez Velazquez Yadhira 

## Licencia

Proyecto desarrollado con fines académicos y educativos.