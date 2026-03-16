echo "Создание директории plots и png"
mkdir -p plots plots/png

echo "Построение графиков (Gnuplot)..."
gnuplot plots/theta_mu.gp
echo "   theta_vs_n_mu.png"

gnuplot plots/theta_lambda.gp
echo "   theta_vs_n_lambda.png"

gnuplot plots/theta_m.gp
echo "   theta_vs_n_m.png"

gnuplot plots/T_mu.gp
echo "   T_vs_n_mu.png"

gnuplot plots/T_lambda.gp
echo "   T_vs_n_lambda.png"

gnuplot plots/T_m.gp
echo "   T_vs_n_m.png"