import pandas as pd
import numpy as np

## Config

OP_TYPE_DEPOSIT = 'Deposit'

EXCHANGE = 'BINANCE'

COIN_TARGET = 'BTC'
COIN_BRL = 'BRL'

TRADE_TYPE_BUY = 'c'
TRADE_TYPE_SELL = 'v'

pd.set_option("display.precision", 8)

## Read settlements

df = pd.read_csv('data/jan-nov-2024.csv')
df = df[(df.Operation != OP_TYPE_DEPOSIT)]
df = df[['Coin', 'Change']]

## Group BRL/TARGET COIN operations

target_df = df[df.Coin == COIN_TARGET].reset_index(drop=True)
brl_df = df[df.Coin == COIN_BRL].reset_index(drop=True)
df_concat = target_df.join(brl_df, lsuffix='_TARGET', rsuffix='_BRL')

## Build trades dataframe

df_concat['Price'] = df_concat.Change_BRL.abs()/df_concat.Change_TARGET.abs()
df_concat['Quantity'] = df_concat.Change_TARGET.abs()
df_concat['Type'] = df_concat.Change_BRL.apply(lambda change : TRADE_TYPE_SELL if change > 0 else TRADE_TYPE_BUY)
df_trades = df_concat[['Price', 'Quantity', 'Type']].reset_index(drop=True)
# df_trades = pd.read_csv('tests/test-1.csv')

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

### Discount Income Tax (IR)
ir = sales_balance * 0.15 if sales_balance > 0 else 0.00

### Investment
investment = mean_price * amm_coins

print(f'Qtd Moedas: {amm_coins:.8}')
print(f'Saldo de Vendas: R$ {sales_balance:.2f}')
print(f'IR: R$ {ir:.2f}')
print(f'Preço médio: R$ {mean_price:.2f}')
print(f"Tenho {amm_coins:.8} {COIN_TARGET}, adquiridos a um custo médio de R$ {mean_price:,.2f}, totalizando um investimento de R$ {investment:,.2f}, custodiados na corretora {EXCHANGE}.")
