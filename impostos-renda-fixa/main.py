from math import floor

# Rendimento bruto em reais
r=0.96

# Numero de dias até o resgate
t=11

# Imposto sobre Operações financeiras
iof = r*(96/100 - t*(3 + 1/3)/100)

# Imposto de Renda (IR)
#   22,50% até 180 dias
#   20,00% entre 180 e 360 dias
#   17,50% entre 361 e 720 dias
#   15,00% acima de 720 dias
n = min(floor((t-1)/180),3)
ir = (r - iof)*((22.5 - 2.50*n)/100)

# Calcular rendimento líquido
final = r - iof - ir

print(f'Rendimento bruto: R$ {r:.2f}')
print(f'IOF: R$ {iof:.2f}')
print(f'IR: R$ {ir:.2f}')
print(f'Rendimento líquido: R$ {final:.2f}')
