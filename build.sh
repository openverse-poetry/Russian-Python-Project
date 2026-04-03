#!/bin/bash
# Скрипт для создания исполняемого файла RusPython

echo "=== Создание исполняемого файла RusPython ==="

# Проверяем наличие PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "Установка PyInstaller..."
    pip install pyinstaller
fi

# Создаем спецификацию и собираем приложение
echo "Сборка исполняемого файла..."
pyinstaller --onefile \
    --name ruspython \
    --add-data "src:src" \
    --hidden-import src.core.lexer \
    --hidden-import src.core.parser \
    --hidden-import src.backend.translator \
    --hidden-import src.runtime.interpreter \
    --hidden-import src.cli.main \
    --console \
    ruspython.py

echo ""
echo "=== Готово! ==="
echo "Исполняемый файл создан в папке dist/"
echo ""
echo "Для запуска:"
echo "  ./dist/ruspython --help"
echo "  ./dist/ruspython examples/hello.ру"
