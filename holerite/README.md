# Holerite

O cálculo do valor líquido é feito da seguinte forma

```
VALOR LÍQUIDO = SALÁRIO BRUTO - DESCONTO INSS - DESCONTO IR - OUTROS DESCONTOS
```

## DESCONTO INSS

```
DESCONTO INSS = (SALÁRIO BRUTO) * ALÍQUOTA - DEDUÇÃO
```

A ALÍQUOTA é definida na faixa de valores em que o SALÁRIO BRUTO se encaixa.

## DESCONTO IR

```
BASE CÁLC IRRF = SALÁRIO BRUTO - DESCONTO SIMPLIFICADO
```

O DESCONTO SIMPLIFICADO é o mesmo no ano. Por exemplo, em 2024-2025, foi de R$ 564,80.

```
DESCONTO IR = (BASE CÁLC IRRF) * ALÍQUOTA - DEDUÇÃO
```

A ALÍQUOTA é definida na faixa de valores em que a BASE CÁLC IRRF se encaixa.

# Exemplo

- Folha: outubro de 2023
- Salário bruto: R$ 1.643,00
- Outros descontos: REFEICAO (R$ 20,00)

Em 2023, tínhamos 

- DESCONTO SIMPLIFICADO: R$ 528,00
- INSS: 9% (com dedução de R$ 19,80), de R$ 1.320,01 até R$ 2.571,29
- IR: ISENTO, até R$ 2.112,00

Logo,

```
BASE CÁLC IRRF = 1.643,00 - 528,00 = R$ 1.115,00
DESCONTO INSS = 1.643,00 * 9% - 19,80 = R$ 128,07
DESCONTO IR = R$ 0,00 (pois, BASE CÁLC IRRF entra na faixa de isenção)
OUTROS DESCONTOS = R$ 20,00
VALOR LÍQUIDO = R$ 1.494,93
```