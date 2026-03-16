#!/bin/bash

echo "Создание директории data"
mkdir -p data plots

echo "Генерация данных (Python)..."
python3 main.py

echo ""
echo "=========================================="
echo "Данные сохранены в папке data/"
ls -lh plots/*.png