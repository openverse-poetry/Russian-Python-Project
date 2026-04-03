@echo off
REM Скачивание и установка Русский Питон в Windows
REM Этот скрипт скачивает последнюю версию с GitHub и устанавливает её

setlocal enabledelayedexpansion

echo ============================================
echo   Загрузка и установка Русский Питон
echo ============================================
echo.

REM Проверяем, установлен ли git
git --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Git найден, используем клонирование...
    
    set "INSTALL_DIR=%USERPROFILE%\ruspython"
    
    if exist "!INSTALL_DIR!" (
        echo Обновление существующей установки...
        cd /d "!INSTALL_DIR!"
        git pull origin main
    ) else (
        echo Клонирование репозитория...
        git clone https://github.com/ruspython/ruspython.git "!INSTALL_DIR!"
        cd /d "!INSTALL_DIR!"
    )
    
    goto :install
)

REM Если git не установлен, пробуем скачать через PowerShell
echo Git не найден, пробуем скачать через PowerShell...
powershell -Command "Get-Command curl" >nul 2>&1
if not errorlevel 1 (
    echo Используем curl для загрузки...
    
    set "INSTALL_DIR=%TEMP%\ruspython"
    if not exist "!INSTALL_DIR!" mkdir "!INSTALL_DIR!"
    cd /d "!INSTALL_DIR!"
    
    REM Скачиваем архив с GitHub
    echo Загрузка последней версии с GitHub...
    curl -L -o ruspython.zip https://github.com/ruspython/ruspython/archive/refs/heads/main.zip
    
    if exist ruspython.zip (
        echo Распаковка архива...
        powershell -Command "Expand-Archive -Path ruspython.zip -DestinationPath . -Force"
        
        REM Переходим в распакованную директорию
        for /d %%i in (ruspython-main) do cd /d "%%i"
        
        goto :install
    ) else (
        echo [ОШИБКА] Не удалось загрузить архив
        goto :manual
    )
) else (
    goto :manual
)

:install
echo.
echo Переход к установке...
cd /d "%~dp0"

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo.
    echo Установите Python 3.8+ с https://www.python.org/downloads/
    echo Не забудьте отметить "Add Python to PATH" при установке
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

REM Устанавливаем зависимости и пакет
echo Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ПРЕДУПРЕЖДЕНИЕ] Не все зависимости установлены, продолжаем...
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
pause
exit /b 0

:manual
echo.
echo ============================================
echo   Ручная установка
echo ============================================
echo.
echo Для установки выполните следующие шаги:
echo.
echo 1. Откройте браузер и перейдите по адресу:
echo    https://github.com/ruspython/ruspython
echo.
echo 2. Нажмите кнопку "Code" и выберите "Download ZIP"
echo.
echo 3. Распакуйте архив в удобную папку
echo.
echo 4. Откройте командную строку в этой папке
echo.
echo 5. Выполните команды:
echo    pip install -r requirements.txt
echo    pip install -e .
echo.
echo После установки будет доступна команда 'ruspython'
echo.
pause
