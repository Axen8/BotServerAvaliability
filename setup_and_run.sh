#!/bin/bash

# Nombre del entorno virtual
VENV_DIR=".venv"

# Archivo de requisitos
REQUIREMENTS_FILE="requirements.txt"

# Archivo principal de tu aplicación
MAIN_SCRIPT="bot.py"

# Crear el entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando el entorno virtual..."
    python3 -m venv "$VENV_DIR"
else
    echo "El entorno virtual ya existe."
fi

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source "$VENV_DIR/bin/activate"

# Instalar dependencias
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Instalando dependencias..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Advertencia: No se encontró el archivo $REQUIREMENTS_FILE."
fi

# Ejecutar la aplicación
if [ -f "$MAIN_SCRIPT" ]; then
    echo "Ejecutando la aplicación..."
    python "$MAIN_SCRIPT"
else
    echo "Error: No se encontró el archivo $MAIN_SCRIPT."
fi

# Desactivar el entorno virtual
echo "Desactivando el entorno virtual..."
deactivate

