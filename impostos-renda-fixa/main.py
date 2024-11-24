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

# Arredondamentos
iof = round(iof, 3)
ir = round(ir, 3)
final = round(final, 3)

print(f'IOF = {iof}, IR = {ir}')
print(f'Rendimento Final = {final}')
