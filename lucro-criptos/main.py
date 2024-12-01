import pandas as pd
import numpy as np
import re

## Config
OP_IGNORED = ['Deposit', 'Transfer Between Main and Funding Wallet']
EXCHANGE = 'BINANCE'
COIN_TARGET = 'BTC'
COIN_BRL = 'BRL'

pd.set_option("display.precision", 8)

## Read settlements
df = pd.read_csv('data/2024-0111-2411.csv')
df = df[~(df['Operation'].isin(OP_IGNORED))]
df = df[['UTC_Time', 'Coin', 'Change']]

## Group BRL/TARGET COIN operations
target_df = df[df['Coin'] == COIN_TARGET].reset_index(drop=True)
brl_df = df[df['Coin'] == COIN_BRL].reset_index(drop=True)
df_concat = target_df.join(brl_df, lsuffix='_TARGET', rsuffix='_BRL')

# Build columns
df_concat['Time'] = df_concat['UTC_Time_TARGET'].apply(lambda ts : pd.Timestamp(ts))
df_concat['Price'] = df_concat['Change_BRL'].abs()/df_concat['Change_TARGET'].abs()
df_concat['Quantity'] = df_concat['Change_TARGET']
df_concat['Investment'] = df_concat['Quantity'].abs() * df_concat['Price']

## Build trades dataframe
df_trades = df_concat[['Time', 'Price', 'Quantity', 'Investment']].reset_index(drop=True)

# Separar vendas de compras
df_buy  = df_trades[df_trades['Quantity'] > 0].copy()
df_sell = df_trades[df_trades['Quantity'] < 0].copy()

# Colunas extras
df_sell['MeanPrice'] = 0.0
df_sell['OwnershipCost'] = 0.0

# Calcular o lucro para cada venda
for idx, row in df_sell.iterrows():
    # Somar valores de linhas anteriores a um timestamp
    calc = lambda dataframe, col : abs(dataframe[dataframe['Time'] < row['Time']][col].sum())

    # Soma do Total gasto nas compras
    inv_buys = calc(df_buy, 'Investment')   

    # Total de moedas compradas
    qt_buys = calc(df_buy, 'Quantity')

    # Total de moedas vendidas
    qt_sells = calc(df_sell, 'Quantity')

    # Soma do Custo de Aquisição
    aq_sells = calc(df_sell, 'OwnershipCost')

    # Preço médio ponderado
    df_sell.loc[idx, 'MeanPrice'] = (inv_buys - aq_sells)/(qt_buys - qt_sells)

    # Custo de Aquisição Total: Preço Médio * Quantidade Vendida
    df_sell.loc[idx, 'OwnershipCost'] = df_sell.loc[idx, 'MeanPrice'] * abs(row['Quantity'])

    # Somar os investimentos relevantes
    df_sell.loc[idx, 'Profit'] = df_sell.loc[idx, 'Investment'] - df_sell.loc[idx, 'OwnershipCost']

print("Compras realizadas:")
print(df_buy)

print("Vendas realizadas com lucros informados:")
print(df_sell)