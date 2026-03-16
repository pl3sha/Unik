# ========================================
# График 1: Пропускная способность
# ========================================
set terminal pngcairo size 1200,800 enhanced font "DejaVu Sans,11"
set output 'bandwidth.png'

set multiplot layout 2,1 rowsfirst

# --- Верхний график: Пропускная способность ---
set logscale x
unset logscale y          # Линейная ось Y для лучшей читаемости!
set xlabel "Размер сообщения" font ",13"
set ylabel "Пропускная способность (МБ/с)" font ",13"
set title "Зависимость пропускной способности от размера сообщения" font ",14"

# Автоматические красивые метки по оси X
set xtics ( \
  "1 B" 1, \
  "8 B" 8, \
  "64 B" 64, \
  "512 B" 512, \
  "4 KB" 4096, \
  "32 KB" 32768, \
  "256 KB" 262144, \
  "2 MB" 2097152, \
  "16 MB" 16777216 \
)
set grid xtics lt 0 lw 1 lc rgb "#dddddd"
set grid ytics lt 0 lw 1 lc rgb "#dddddd"
set key top left font ",12"

plot '1level.txt' using 1:3 with linespoints pt 7 ps 1.2 lw 2 lc rgb '#2E7D32' title 'Уровень 1: Контроллер памяти', \
     '2level.txt' using 1:3 with linespoints pt 9 ps 1.2 lw 2 lc rgb '#F57C00' title 'Уровень 2: Внутрисистемная шина', \
     '3level.txt' using 1:3 with linespoints pt 11 ps 1.2 lw 2 lc rgb '#C62828' title 'Уровень 3: Сетевой адаптер (GigE)'

# --- Нижний график: Время передачи (латентность) ---
set logscale y            # Для времени оставляем логарифмическую ось Y (диапазон большой)
set xlabel "Размер сообщения" font ",13"
set ylabel "Время передачи (мкс)" font ",13"
set title "Зависимость времени передачи t(m) от размера сообщения" font ",14"

plot '1level.txt' using 1:4 with linespoints pt 7 ps 1.2 lw 2 lc rgb '#2E7D32' title 'Уровень 1: Контроллер памяти', \
     '2level.txt' using 1:4 with linespoints pt 9 ps 1.2 lw 2 lc rgb '#F57C00' title 'Уровень 2: Внутрисистемная шина', \
     '3level.txt' using 1:4 with linespoints pt 11 ps 1.2 lw 2 lc rgb '#C62828' title 'Уровень 3: Сетевой адаптер (GigE)'

unset multiplot