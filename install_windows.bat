@echo off
REM Установка Русского Питона в Windows
REM Запустите этот файл для автоматической установки

setlocal enabledelayedexpansion

echo ============================================
echo   Установка Русский Питон v1.0.0
echo ============================================
echo.

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo.
    echo Пожалуйста, установите Python 3.8+ с официального сайта:
    echo https://www.python.org/downloads/
    echo.
    echo При установке отметьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo [OK] Python найден
python --version
echo.

REM Проверяем pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] pip не найден!
    echo.
    echo Попробуйте установить pip:
    echo python -m ensurepip --upgrade
    pause
    exit /b 1
)

echo [OK] pip найден
echo.

REM Обновляем pip
echo Обновление pip...
python -m pip install --upgrade pip
echo.

REM Определяем директорию установки
set "INSTALL_DIR=%~dp0"
cd /d "%INSTALL_DIR%"

echo Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить зависимости
    pause
    exit /b 1
)
echo.

echo Установка Русский Питон...
pip install -e .
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить пакет
    pause
    exit /b 1
)
echo.

echo ============================================
echo   Установка завершена успешно!
echo ============================================
echo.
echo Теперь вы можете использовать команду 'ruspython' в любом месте:
echo   ruspython примеры/hello.ру
echo   ruspython --repl
echo   ruspython --help
echo.
echo Или используйте batch-файл:
echo   ruspython.bat примеры/hello.ру
echo.
pause
