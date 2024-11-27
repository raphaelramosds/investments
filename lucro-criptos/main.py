import pandas as pd
import numpy as np

## Config

OP_IGNORED = ['Deposit', 'Transfer Between Main and Funding Wallet']
EXCHANGE = 'BINANCE'
COIN_TARGET = 'BTC'
COIN_BRL = 'BRL'
TRADE_TYPE_BUY = 'c'
TRADE_TYPE_SELL = 'v'

pd.set_option("display.precision", 8)

## Read settlements

df = pd.read_csv('data/2024-0111-2411.csv')
df = df[~(df.Operation.isin(OP_IGNORED))]
df = df[['Coin', 'Change']]

## Group BRL/TARGET COIN operations

target_df = df[df.Coin == COIN_TARGET].reset_index(drop=True)
brl_df = df[df.Coin == COIN_BRL].reset_index(drop=True)
df_concat = target_df.join(brl_df, lsuffix='_TARGET', rsuffix='_BRL')

## Build trades dataframe

df_concat['Price'] = df_concat.Change_BRL.abs()/df_concat.Change_TARGET.abs()
df_concat['Quantity'] = df_concat.Change_TARGET.abs()
df_concat['Investment'] = df_concat.Change_BRL
df_concat['Profit'] = df_concat['Investment'].cumsum()
df_concat['Type'] = df_concat.Change_BRL.apply(lambda change : TRADE_TYPE_SELL if change > 0 else TRADE_TYPE_BUY)
df_concat['Tax'] = df_concat.Profit.apply(lambda profit : 0.15*profit if profit > 0 else 0)

df_trades = df_concat[['Price', 'Quantity', 'Investment', 'Type', 'Profit', 'Tax']].reset_index(drop=True)

df_buy_trades = df_trades[df_trades.Type == TRADE_TYPE_BUY]
total_buy = (df_buy_trades.Price * df_buy_trades.Quantity).sum()

df_sell_trades = df_trades[df_trades.Type == TRADE_TYPE_SELL]
total_sell = (df_sell_trades.Price * df_sell_trades.Quantity).sum()

## Statistics

### Coin mean price
mean_price = total_buy/df_buy_trades.Quantity.sum()

### Amount of coins
amm_coins = (np.where(df_trades.Type == TRADE_TYPE_BUY, df_trades.Quantity, (-1) * df_trades.Quantity)).sum()

### Sales balance
sales_balance = total_sell - mean_price * df_sell_trades.Quantity.sum()

### Investment
investment = mean_price * amm_coins

print("Declaração IR:")
print(f"Tenho {amm_coins:.8} {COIN_TARGET}, adquiridos a um custo médio de R$ {mean_price:,.2f}, totalizando um investimento de R$ {investment:,.2f}, custodiados na corretora {EXCHANGE}.")

print(f"Quadro de aplicações:")
print(df_trades)