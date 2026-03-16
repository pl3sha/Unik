#!/bin/bash

if [ ! -f "main.py" ]; then
    echo "Ошибка: файл main.py не найден"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Запуск с параметрами по умолчанию..."
    python3 main.py "$1"
elif [ $# -eq 1 ] && [ -f "$1" ]; then
    echo "Запуск из файла: $1"
    python3 main.py "$1"
else
    echo "Запуск с аргументами: $@"
    python3 main.py "$@"
fi

echo ""
echo "Готово."