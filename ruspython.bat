@echo off
REM Русский Питон - Точка входа для Windows
REM Использование: ruspython.bat [файл.ру] [опции]

setlocal enabledelayedexpansion

REM Определяем путь к текущей директории
set "SCRIPT_DIR=%~dp0"

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не найден. Пожалуйста, установите Python 3.8+
    echo Скачайте с https://www.python.org/downloads/
    exit /b 1
)

REM Запускаем ruspython.py с передачей всех аргументов
python "%SCRIPT_DIR%ruspython.py" %*
