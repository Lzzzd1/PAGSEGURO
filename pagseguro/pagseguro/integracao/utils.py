def calcular_juros(valor, parcelas):
    if int(parcelas) > 1:
        taxa_juros = 1.67 / 100  # 1,67% em decimal

        valor_total = valor * (1 + taxa_juros) ** int(parcelas)
        return int(valor_total)
    return valor


def calcular_parcelas(valor_total, parcelas):
    valor_parcela = valor_total / parcelas
    return valor_parcela
