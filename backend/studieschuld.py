#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 15:10:18 2022

@author: asp
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

DEBT_BSC = 41899.78
DEBT_MSC = 2406.86 + 11903.13
DEBT_PRESTATIEBEURS = 439.20 + 1509.43
MONTHLY_LOAN_MSC_2023_AUTUMN = 682.97 + 192.83
MONTHLY_PRESTATIEBEURS_2023_AUTUMN = 120.96 + 439.20
MONTHLY_LOAN_MSC_2024_SPRING = 751.27 + 192.83
MONTHLY_PRESTATIEBEURS_2024_SPRING = 466.69 + 120.96
MONTHLY_LOAN_MSC_2024_AUTUMN = 751.27 + 210.83
TODAY = datetime.date.today()
END_DATE_ZERO_PERCENT = datetime.date(2026, 12, 31)
END_DATE_STUDY = datetime.date(2024, 10, 31)
END_DATE_LOAN_MSC = datetime.date(2023, 12, 31)

INTEREST_RATES = [
    [2024, 2.56],
    [2023, 0.46],
    [2022, 0.00],
    [2021, 0.00],
    [2020, 0.00],
    [2019, 0.00],
    [2018, 0.00],
    [2017, 0.00],
    [2016, 0.01],
    [2015, 0.12],
    [2014, 0.81],
    [2013, 0.60],
    [2012, 1.39],
    [2011, 1.50],
    [2010, 2.39],
    [2009, 3.58],
    [2008, 4.17],
    [2007, 3.70],
    [2006, 2.74]
]

def total_debt_func(init, final, interest_bool=True):
    T = np.arange(init, final, 1/12)
    
    total_debt = np.zeros(len(T))
    debt_bachelor = np.zeros(len(T))
    debt_prestatiebeurs = np.zeros(len(T))
    debt_master = np.zeros(len(T))

    debt_bachelor[0] = DEBT_BSC
    debt_prestatiebeurs[0] = DEBT_PRESTATIEBEURS
    debt_master[0] = DEBT_MSC
    total_debt[0] = debt_bachelor[0] + debt_prestatiebeurs[0] + debt_master[0]
    
    time = np.zeros(len(T))
    time[0] = init
    
    for i, t in enumerate(T):
        if i == 0:
            continue
        current_year = int(t // 1)
        current_month = int((t % 1) * 12) + 1
        time[i] = t
        if current_year > END_DATE_STUDY.year or (current_year == END_DATE_STUDY.year and current_month > END_DATE_STUDY.month):
            monthly_loan_prestatie = 0
            monthly_loan_msc = 0
        elif current_year > END_DATE_LOAN_MSC.year or (current_year == END_DATE_LOAN_MSC.year and current_month > END_DATE_LOAN_MSC.month):
            monthly_loan_msc = 0
        elif current_year < 2023:
            monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2023_AUTUMN
            monthly_loan_msc = MONTHLY_LOAN_MSC_2023_AUTUMN
        elif current_year == 2023:
            if current_month < 9:
                monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2023_AUTUMN
                monthly_loan_msc = MONTHLY_LOAN_MSC_2023_AUTUMN
            else:
                monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING
                monthly_loan_msc = MONTHLY_LOAN_MSC_2024_SPRING
        elif current_year >= 2024:
            if current_month < 9:
                monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING
                monthly_loan_msc = MONTHLY_LOAN_MSC_2024_SPRING
            else:
                monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING
                monthly_loan_msc = MONTHLY_LOAN_MSC_2024_AUTUMN


        if interest_bool:
            if current_year <= END_DATE_ZERO_PERCENT.year:
                interest_rate_bsc = INTEREST_RATES[2][1] / 100 / 12
            elif current_year < 2023:
                interest_rate_bsc = INTEREST_RATES[2][1] / 100 / 12
            elif current_year == 2023:
                interest_rate_bsc = INTEREST_RATES[1][1] / 100 / 12
            elif current_year >= 2024:
                interest_rate_bsc = INTEREST_RATES[0][1] / 100 / 12
            debt_bachelor[i] = debt_bachelor[i-1] + debt_bachelor[i-1] * interest_rate_bsc

            if current_year < 2023:
                interest_rate_msc = INTEREST_RATES[2][1] / 100 / 12
            elif current_year == 2023:
                interest_rate_msc = INTEREST_RATES[1][1] / 100 / 12
            elif current_year >= 2024:
                interest_rate_msc = INTEREST_RATES[0][1] / 100 / 12
            #set to zero if study is completed
            if current_year > END_DATE_STUDY.year or (current_year == END_DATE_STUDY.year and current_month > END_DATE_STUDY.month):
                debt_prestatiebeurs[i] = 0
            else:
                debt_prestatiebeurs[i] = debt_prestatiebeurs[i-1] + debt_prestatiebeurs[i-1] * interest_rate_msc + monthly_loan_prestatie
            debt_master[i] = debt_master[i-1] + debt_master[i-1] * interest_rate_msc + monthly_loan_msc
        
        else:
            if current_year > END_DATE_STUDY.year or (current_year == END_DATE_STUDY.year and current_month > END_DATE_STUDY.month):
                debt_prestatiebeurs[i] = 0
            else:
                debt_prestatiebeurs[i] = debt_prestatiebeurs[i-1] + monthly_loan_prestatie
            debt_bachelor[i] = debt_bachelor[i-1]
            debt_master[i] = debt_master[i-1] + monthly_loan_msc

        total_debt[i] = debt_bachelor[i] + debt_prestatiebeurs[i] + debt_master[i]

    return time, total_debt, debt_bachelor, debt_prestatiebeurs, debt_master

init = TODAY.year + TODAY.month/12
final = TODAY.year + TODAY.month/12 + 10
time, total_debt, debt_bachelor, debt_prestatiebeurs, debt_master = total_debt_func(init, final)
time2, total_debt2, _, _, _ = total_debt_func(init, final, interest_bool=False)

fig, ax = plt.subplots()
ax.plot(time, total_debt, label='with interest')
ax.plot(time2, total_debt2, label='without interest')
ax.grid()
x_end = END_DATE_STUDY.year + END_DATE_STUDY.month/12
ax.axvline(x=x_end, color='k', linestyle='--')
ax.set_ylabel('Euros')
ax.set_xlabel('Year')
ax.legend()
ax.set_title('Total Debt')
plt.show()


# plot debts
fig, ax = plt.subplots()
plt.plot(time, debt_bachelor, label='bachelor')
plt.plot(time, debt_prestatiebeurs, label='prestatiebeurs')
plt.plot(time, debt_master, label='master')
plt.grid()
x_end = END_DATE_STUDY.year + END_DATE_STUDY.month/12
plt.axvline(x=x_end, color='k', linestyle='--')
plt.ylabel('Euros')
plt.xlabel('Year')
plt.legend()
plt.title('Debts')
plt.show()

# plot difference
fig, ax = plt.subplots()
plt.plot(time, total_debt-total_debt2, label='difference')
plt.grid()
x_end = END_DATE_STUDY.year + END_DATE_STUDY.month/12
plt.axvline(x=x_end, color='k', linestyle='--')
plt.ylabel('Euros')
plt.xlabel('Year')
plt.legend()
plt.title('Difference')
plt.show()


df = pd.DataFrame({'time':np.round(time,decimals=2),
                   'debt withou interest':np.round(total_debt2,decimals=2),
                   'debt with interest':np.round(total_debt,decimals=2),
                   'difference':np.round(total_debt-total_debt2,decimals=2)})

#df.to_csv(r'/home/asp/Downloads/debt.csv', sep=',')
















