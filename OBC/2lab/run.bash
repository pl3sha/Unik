#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "${CYAN}[STEP]${NC} $1"; }

# Проверка Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 не найден!"
    exit 1
fi
log_success "Python 3 найден: $(python3 --version)"

# Проверка зависимостей
log_step "Проверка зависимостей..."
python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    log_warn "matplotlib не установлен. Установка..."
    pip3 install matplotlib --quiet
fi

python3 -c "import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    log_warn "numpy не установлен. Установка..."
    pip3 install numpy --quiet
fi
log_success "Все зависимости установлены"

# Проверка файлов
log_step "Проверка файлов..."
if [ ! -f "main.py" ]; then
    log_error "Файл main.py не найден!"
    exit 1
fi

if [ ! -f "plot.py" ]; then
    log_error "Файл plot.py не найден!"
    exit 1
fi
log_success "Все файлы найдены"

# Создание директорий
log_step "Создание директорий для результатов..."
mkdir -p results/schedules
mkdir -p results/graphs
mkdir -p results/data
mkdir -p results/logs

# Тестовый файл
log_step "Создание тестового файла tasks.txt..."
cat > tasks.txt << EOF
50 10
30 20
40 15
20 25
60 5
45 12
35 18
25 22
55 8
40 14
EOF

# Задание 1: Тест алгоритмов
echo ""
log_step "ЗАДАНИЕ 1: Тест алгоритмов..."
python3 main.py tasks.txt 1024 NFDH 2>&1 | tee results/logs/nfdh_test.log
python3 main.py tasks.txt 1024 FFDH 2>&1 | tee results/logs/ffdh_test.log

# Задание 2-3: Эксперименты
echo ""
log_step "ЗАДАНИЯ 2-3: Эксперименты (может занять 30-60 минут)..."
python3 plot.py 2>&1 | tee results/logs/plot.log

# Перемещение графиков
mv *.png results/graphs/ 2>/dev/null
mv *.csv results/data/ 2>/dev/null

echo ""
log_success "Выполнение завершено!"
echo ""
log_info "Результаты в папке: results/"
ls -la results/graphs/ 2>/dev/null