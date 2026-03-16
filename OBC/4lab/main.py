#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def calculate_mu_l(l, N, m, mu):
    if N - m <= l <= N:
        return (N - l) * mu
    else:
        return m * mu

def calculate_theta(N, n, lambda_val, mu, m):
    theta = 1.0 / lambda_val
    for j in range(n, N):
        mu_j = calculate_mu_l(j, N, m, mu)
        product = 1.0
        for l in range(n, j + 1):
            mu_l = calculate_mu_l(l, N, m, mu)
            product *= lambda_val / mu_l
        theta += (1.0 / mu_j) * product
    return theta

def calculate_T(N, n, lambda_val, mu, m):
    if n == 1:
        return 1.0 / calculate_mu_l(0, N, m, mu)
    T = 0.0
    for j in range(0, n):
        product = 1.0
        for l in range(j + 1, n):
            lambda_l = lambda_val
            mu_l = calculate_mu_l(l, N, m, mu)
            product *= lambda_l / mu_l
        sum_part = sum(1.0 / lambda_val for _ in range(j + 1, n + 1))
        mu_j = calculate_mu_l(j, N, m, mu)
        T += (1.0 / mu_j) * product * sum_part
    return T

def generate_theta_dat_2_1():
    N = 65536
    lambda_val = 1e-5
    m = 1
    mu_values = [1, 10, 100, 1000]
    for mu in mu_values:
        filename = f'data/theta_mu{mu}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tTheta\n')
            for n in range(65527, 65537):
                theta = calculate_theta(N, n, lambda_val, mu, m)
                f.write(f'{n}\t{theta:.6e}\n')

def generate_theta_dat_2_2():
    N = 65536
    mu = 1
    m = 1
    lambda_values = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    for lam in lambda_values:
        lam_str = str(lam).replace('.', '_').replace('-', '')
        filename = f'data/theta_lambda{lam_str}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tTheta\n')
            for n in range(65527, 65537):
                theta = calculate_theta(N, n, lam, mu, m)
                f.write(f'{n}\t{theta:.6e}\n')

def generate_theta_dat_2_3():
    N = 65536
    mu = 1
    lambda_val = 1e-5
    m_values = [1, 2, 3, 4]
    for m_val in m_values:
        filename = f'data/theta_m{m_val}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tTheta\n')
            for n in range(65527, 65537):
                theta = calculate_theta(N, n, lambda_val, mu, m_val)
                f.write(f'{n}\t{theta:.6e}\n')

def generate_T_dat_3_1():
    N = 1000
    lambda_val = 1e-3
    m = 1
    mu_values = [1, 2, 4, 6]
    for mu in mu_values:
        filename = f'data/T_mu{mu}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tT\n')
            for n in range(900, 1001, 10):
                T = calculate_T(N, n, lambda_val, mu, m)
                f.write(f'{n}\t{T:.6e}\n')

def generate_T_dat_3_2():
    N = 8192
    mu = 1
    m = 1
    lambda_values = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    for lam in lambda_values:
        lam_str = str(lam).replace('.', '_').replace('-', '')
        filename = f'data/T_lambda{lam_str}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tT\n')
            for n in range(8092, 8193, 10):
                T = calculate_T(N, n, lam, mu, m)
                f.write(f'{n}\t{T:.6e}\n')

def generate_T_dat_3_3():
    N = 8192
    mu = 1
    lambda_val = 1e-5
    m_values = [1, 2, 3, 4]
    for m_val in m_values:
        filename = f'data/T_m{m_val}.dat'
        with open(filename, 'w') as f:
            f.write('# n\tT\n')
            for n in range(8092, 8193, 10):
                T = calculate_T(N, n, lambda_val, mu, m_val)
                f.write(f'{n}\t{T:.6e}\n')

def main():
    os.makedirs('data', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    print('Generating data files...')
    generate_theta_dat_2_1()
    generate_theta_dat_2_2()
    generate_theta_dat_2_3()
    generate_T_dat_3_1()
    generate_T_dat_3_2()
    generate_T_dat_3_3()
    print('Data files generated in data/ directory')

if __name__ == '__main__':
    main()