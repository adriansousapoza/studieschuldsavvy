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
import plotly.graph_objects as go
import requests
import json

def total_debt_func(init, final, 
                    DEBT_BSC, 
                    DEBT_MSC, 
                    DEBT_PRESTATIEBEURS, MONTHLY_LOAN_MSC_2023_AUTUMN, 
                    MONTHLY_PRESTATIEBEURS_2023_AUTUMN,
                    MONTHLY_LOAN_MSC_2024_SPRING,
                    MONTHLY_PRESTATIEBEURS_2024_SPRING,
                    MONTHLY_LOAN_MSC_2024_AUTUMN,
                    END_DATE_STUDY, 
                    END_DATE_LOAN_MSC, 
                    END_DATE_ZERO_PERCENT,
                    INTEREST_RATES,
                    interest_bool=True):
    T = np.arange(init, final, 1/12)
    
    total_debt = np.zeros(len(T))
    debt_bachelor = np.zeros(len(T))
    debt_prestatiebeurs = np.zeros(len(T))
    debt_master = np.zeros(len(T))

    debt_bachelor[0] = DEBT_BSC
    debt_prestatiebeurs[0] = DEBT_MSC
    debt_master[0] = DEBT_PRESTATIEBEURS
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

def plot_total_debt(time, total_debt, total_debt2, x_end):
    trace1 = go.Scatter(x=time, y=total_debt, mode='lines', name='with interest')
    trace2 = go.Scatter(x=time, y=total_debt2, mode='lines', name='without interest')
    line = go.Scatter(x=[x_end, x_end], y=[0, max(max(total_debt), max(total_debt2))], 
                      mode='lines', line=dict(dash='dash'), name='End Study')

    data = [trace1, trace2, line]

    layout = go.Layout(
        title='Total Debt',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euros'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def plot_individual_debts(time, debt_bachelor, debt_prestatiebeurs, debt_master, x_end):
    trace1 = go.Scatter(x=time, y=debt_bachelor, mode='lines', name='bachelor')
    trace2 = go.Scatter(x=time, y=debt_prestatiebeurs, mode='lines', name='prestatiebeurs')
    trace3 = go.Scatter(x=time, y=debt_master, mode='lines', name='master')
    line = go.Scatter(x=[x_end, x_end], y=[0, max(max(debt_bachelor), max(debt_prestatiebeurs), max(debt_master))], 
                      mode='lines', line=dict(dash='dash'), name='End Study')

    data = [trace1, trace2, trace3, line]

    layout = go.Layout(
        title='Debts',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euros'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def plot_debt_difference(time, total_debt, total_debt2, x_end):
    difference = [td - td2 for td, td2 in zip(total_debt, total_debt2)]

    trace1 = go.Scatter(x=time, y=difference, mode='lines', name='difference')
    line = go.Scatter(x=[x_end, x_end], y=[0, max(difference)], 
                      mode='lines', line=dict(dash='dash'), name='End Study')

    data = [trace1, line]

    layout = go.Layout(
        title='Difference',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euros'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def plot_inflation_rates(periods, inflation_rates):
    trace_inflation = go.Scatter(x=periods, y=inflation_rates, mode='lines', name='Inflation Rate')

    data = [trace_inflation]

    layout = go.Layout(
        title='Inflation Rates Over Time',
        xaxis=dict(title='Period'),
        yaxis=dict(title='Inflation Rate (%)'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def get_inflation_rates():
    base_url = 'https://opendata.cbs.nl/ODataApi/OData/70936ned/'
    collection = 'TypedDataSet'
    data = None

    collection_url = f"{base_url}{collection}"
    response = requests.get(collection_url)

    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        print(f"Failed to retrieve data from {collection}. Status code: {response.status_code}")

    if data is not None:
        inflation_info = []
        for record in data['value']:
            period_str = record['Perioden']
            year, month = int(period_str[:4]), int(period_str[6:8])
            if year >= 2006 and month != 0:
                period_date = datetime.datetime(year, month, 1)
                formatted_period = period_date.strftime('%m/%Y')

                inflation_info.append({
                    'period': formatted_period,
                    'inflation_rate': record['JaarmutatieCPI_1']
                })

        periods = [info['period'] for info in inflation_info]
        inflation_rates = [info['inflation_rate'] for info in inflation_info]

        return periods, inflation_rates

        
    else:
        print("Data retrieval failed. 'data' is not set.")
        return None, None
    
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
    
init = TODAY.year + TODAY.month/12
final = TODAY.year + TODAY.month/12 + 10
time, total_debt, debt_bachelor, debt_prestatiebeurs, debt_master = total_debt_func(init, final, DEBT_BSC=DEBT_BSC, DEBT_MSC=DEBT_MSC, DEBT_PRESTATIEBEURS=DEBT_PRESTATIEBEURS, MONTHLY_LOAN_MSC_2023_AUTUMN=MONTHLY_LOAN_MSC_2023_AUTUMN, MONTHLY_PRESTATIEBEURS_2023_AUTUMN=MONTHLY_PRESTATIEBEURS_2023_AUTUMN, MONTHLY_LOAN_MSC_2024_SPRING=MONTHLY_LOAN_MSC_2024_SPRING, MONTHLY_PRESTATIEBEURS_2024_SPRING=MONTHLY_PRESTATIEBEURS_2024_SPRING, MONTHLY_LOAN_MSC_2024_AUTUMN=MONTHLY_LOAN_MSC_2024_AUTUMN, END_DATE_STUDY=END_DATE_STUDY, END_DATE_LOAN_MSC=END_DATE_LOAN_MSC, END_DATE_ZERO_PERCENT=END_DATE_ZERO_PERCENT, INTEREST_RATES=INTEREST_RATES)
time2, total_debt2, _, _, _ = total_debt_func(init, final, DEBT_BSC=DEBT_BSC, DEBT_MSC=DEBT_MSC, DEBT_PRESTATIEBEURS=DEBT_PRESTATIEBEURS, MONTHLY_LOAN_MSC_2023_AUTUMN=MONTHLY_LOAN_MSC_2023_AUTUMN, MONTHLY_PRESTATIEBEURS_2023_AUTUMN=MONTHLY_PRESTATIEBEURS_2023_AUTUMN, MONTHLY_LOAN_MSC_2024_SPRING=MONTHLY_LOAN_MSC_2024_SPRING, MONTHLY_PRESTATIEBEURS_2024_SPRING=MONTHLY_PRESTATIEBEURS_2024_SPRING, MONTHLY_LOAN_MSC_2024_AUTUMN=MONTHLY_LOAN_MSC_2024_AUTUMN, END_DATE_STUDY=END_DATE_STUDY, END_DATE_LOAN_MSC=END_DATE_LOAN_MSC, END_DATE_ZERO_PERCENT=END_DATE_ZERO_PERCENT, INTEREST_RATES=INTEREST_RATES, interest_bool=False)
x_end = END_DATE_STUDY.year + END_DATE_STUDY.month/12

debt_fig = plot_total_debt(time, total_debt, total_debt2, x_end)
debt_individual_fig = plot_individual_debts(time, debt_bachelor, debt_prestatiebeurs, debt_master, x_end)
debt_difference_fig = plot_debt_difference(time, total_debt, total_debt2, x_end)

df = pd.DataFrame({'time':np.round(time,decimals=2),
                   'debt withou interest':np.round(total_debt2,decimals=2),
                   'debt with interest':np.round(total_debt,decimals=2),
                   'difference':np.round(total_debt-total_debt2,decimals=2)})

#df.to_csv(r'/home/asp/Downloads/debt.csv', sep=',')

periods, inflation_rates = get_inflation_rates()
inflation_plot = plot_inflation_rates(periods, inflation_rates)

#debt_fig.show()
#debt_individual_fig.show()
#debt_difference_fig.show()
#inflation_plot.show()