import pandas as pd
import numpy as np
import re

## Config
OP_IGNORED = ['Deposit', 'Transfer Between Main and Funding Wallet']
EXCHANGE = 'BINANCE'
COIN_TARGET = 'BTC'
COIN_BRL = 'BRL'
TRADE_TYPE_BUY = 'compra'
TRADE_TYPE_SELL = 'venda'

pd.set_option("display.precision", 8)

## Read settlements
df = pd.read_csv('data/2024-0111-2411.csv')
df = df[~(df.Operation.isin(OP_IGNORED))]
df = df[['UTC_Time', 'Coin', 'Change']]

## Group BRL/TARGET COIN operations
target_df = df[df.Coin == COIN_TARGET].reset_index(drop=True)
brl_df = df[df.Coin == COIN_BRL].reset_index(drop=True)
df_concat = target_df.join(brl_df, lsuffix='_TARGET', rsuffix='_BRL')

# Build columns
df_concat['Time'] = df_concat.UTC_Time_TARGET
df_concat['Price'] = df_concat.Change_BRL.abs()/df_concat.Change_TARGET.abs()
df_concat['Quantity'] = df_concat.Change_TARGET.abs()
df_concat['Type'] = df_concat.Change_BRL.apply(lambda change : TRADE_TYPE_SELL if change > 0 else TRADE_TYPE_BUY)
df_concat['Investment'] = df_concat.Quantity * df_concat.Price

## Build trades dataframe
df_trades = df_concat[['Time', 'Price', 'Quantity', 'Type', 'Investment']].reset_index(drop=True)

# Quadro de operações
print(df_trades)
