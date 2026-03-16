#!/usr/bin/gnuplot -persist

set terminal pngcairo size 1200,800 font "Arial,14"
set output 'oak_bandwidth.png'

# Настройка заголовка и осей
set title "Зависимость пропускной способности от размера сообщения" font "Arial Bold,16"
set xlabel "Размер сообщения" font "Arial,14"
set ylabel "Пропускная способность (МБ/с)" font "Arial,14"

# Логарифмическая шкала по X
set logscale x
set grid

# Кастомные метки на оси X (как в вашем примере)
set xtics ("1 Б" 1, "8 Б" 8, "64 Б" 64, "512 Б" 512, "4 КБ" 4096, "32 КБ" 32768, "256 КБ" 262144, "2 МБ" 2097152, "16 МБ" 16777216)

# Легенда
set key top left font "Arial,12" box width 1.5

# Построение графиков
plot \
  'oak_level1.dat' using 1:3 with linespoints lc rgb "#2E7D32" lw 2 pt 7 ps 0.8 title "Уровень 1: Контроллер памяти", \
  'oak_level2.dat' using 1:3 with linespoints lc rgb "#1976D2" lw 2 pt 9 ps 0.8 title "Уровень 2: Внутрисистемная шина", \
  'oak_level3.dat' using 1:3 with linespoints lc rgb "#C62828" lw 2 pt 11 ps 0.8 title "Уровень 3: Сетевой адаптер (GigE)"
