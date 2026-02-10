# CURSO DE FastMCP - MCP SERVER CUSTOM
## 1. Instalación de UV de Astro

UV es un gestor de paquetes para proyectos de JavaScript y TypeScript. Se utiliza para instalar y gestionar dependencias en el proyecto de FastMCP.

### Comando de instalación

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Paso 1: Verificar la carpeta de instalación

El instalador debería haber puesto los archivos en:

```
C:\Users\lftob\.local\bin
```

Verifica con:

```cmd
dir C:\Users\lftob\.local\bin
```

Deberías ver:
- `uv.exe`
- `uvx.exe`
- `uvw.exe`

### Paso 2: Agregar a PATH (recomendado)

1. Presiona la tecla Windows
2. Escribe "Editar variables de entorno"
3. Abre "Editar las variables de entorno del sistema"
4. Haz clic en "Variables de entorno..."
5. Bajo "Variables de usuario para lftob":
    - Selecciona `Path`
    - Haz clic en "Editar"
    - Haz clic en "Nuevo"
    - Agrega: `C:\Users\lftob\.local\bin`

## Creación de 2 archivos para el proyecto de FastMCP
Primero se crea el proyecto python:
```
uv init
uv venv
uv add fastmcp
uv add psycopg2
```



