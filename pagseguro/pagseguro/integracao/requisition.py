from pagseguro.integracao.utils import calcular_juros

import datetime

import requests

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer B3BC2839DB814D8EA24C869035E1DEB3"
}


def get_key():
    url = "https://sandbox.api.pagseguro.com/public-keys"

    body = {'type': 'card'}

    response = requests.post(url, headers=headers, json=body)

    return response.json()['public_key']


def gerar_boleto(valor, **kwargs):
    tel = kwargs.get('telefone')
    body = {
        "reference_id": "ex-00001",
        "customer": {
            "name": kwargs.get('nome'),
            "email": kwargs.get('email'),
            "tax_id": kwargs.get('cpf').replace('-', '').replace('.', '').replace(' ', ''),
            "phones": [
                {
                    "country": "55",
                    "area": tel[:2] if not tel.startswith('55') else tel[2:4],
                    "number": tel[2:] if not tel.startswith('55') else tel[4:],
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "reference_id": "referencia do item",
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 500
            }
        ],
        "shipping": {
            "address": {
                "street": kwargs.get('endereco'),
                "number": kwargs.get('numero'),
                "complement": kwargs.get('complemento'),
                "locality": kwargs.get('bairro'),
                "city": kwargs.get('cidade'),
                "region_code": kwargs.get('uf'),
                "country": "BRA",
                "postal_code": kwargs.get('cep'),
            }
        },
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ],
        "charges": [
            {
                "reference_id": "referencia da cobranca",
                "description": "descricao da cobranca",
                "amount": {
                    "value": valor,
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "BOLETO",
                    "boleto": {
                        "due_date": (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                        "instruction_lines": {
                            "line_1": "Pagamento processado para DESC Fatura",
                            "line_2": "Via PagSeguro"
                        },
                        "holder": {
                            "name": kwargs.get('nome'),
                            "tax_id": kwargs.get('cpf').replace('-', '').replace('.', '').replace(' ', ''),
                            "email": kwargs.get('email'),
                            "address": {
                                "country": "Brasil",
                                "region": kwargs.get('uf'),
                                "region_code": kwargs.get('uf'),
                                "city": kwargs.get('cidade'),
                                "postal_code": kwargs.get('cep'),
                                "street": kwargs.get('endereco'),
                                "number": kwargs.get('numero'),
                                "locality": kwargs.get('bairro')
                            }
                        }
                    }
                }
            }
        ]
    }

    resposta = requests.post('https://sandbox.api.pagseguro.com/orders', json=body, headers=headers)
    print(body)
    return resposta.json()


def gerar_pix(valor, **kwargs):
    tel = kwargs.get('telefone')
    body = {"reference_id": "ex-00001",
            "customer": {
                "name": kwargs.get('nome'),
                "email": kwargs.get('email'),
                "tax_id": kwargs.get('cpf').replace('-', '').replace('.', '').replace(' ', ''),
                "phones": [
                    {
                        "country": "55",
                        "area": tel[:2] if not tel.startswith('55') else tel[2:4],
                        "number": tel[2:] if not tel.startswith('55') else tel[4:],
                        "type": "MOBILE"
                    }
                ]
            },
            "items": [
                {
                    "name": "nome do item",
                    "quantity": 1,
                    "unit_amount": 500
                }
            ],
            "qr_codes": [
                {
                    "amount": {
                        "value": valor
                    },
                    "expiration_date": (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'
                                                                                                     ':%S-03:00'),
                }
            ],
            "shipping": {
                "address": {
                    "country": "BRA",
                    "region": kwargs.get('uf'),
                    "region_code": kwargs.get('uf'),
                    "city": kwargs.get('cidade'),
                    "postal_code": kwargs.get('cep'),
                    "street": kwargs.get('endereco'),
                    "number": kwargs.get('numero'),
                    "locality": kwargs.get('bairro')
                }
            },
            "notification_urls": [
                "https://meusite.com/notificacoes"
            ]

            }
    resposta = requests.post('https://sandbox.api.pagseguro.com/orders', json=body, headers=headers)
    return resposta.json()


def gerar_cartao(valor, **kwargs):
    valor = calcular_juros(valor, int(kwargs.get('parcelas', 1)))
    tel = kwargs.get('telefone')
    body = {
        "reference_id": "ex-00001",
        "customer": {
            "name": kwargs.get('nome'),
            "email": kwargs.get('email'),
            "tax_id": kwargs.get('cpf').replace('-', '').replace('.', '').replace(' ', ''),
            "phones": [
                {
                    "country": "55",
                    "area": tel[:2] if not tel.startswith('55') else tel[2:4],
                    "number": tel[2:] if not tel.startswith('55') else tel[4:],
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "reference_id": "referencia do item",
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 500
            }
        ],
        "shipping": {
            "address": {
                "street": kwargs.get('endereco'),
                "number": kwargs.get('numero'),
                "complement": kwargs.get('complemento'),
                "locality": kwargs.get('bairro'),
                "city": kwargs.get('cidade'),
                "region_code": kwargs.get('uf'),
                "country": "BRA",
                "postal_code": kwargs.get('cep'),
            }
        },
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ],
        "charges": [
            {
                "reference_id": "referencia da cobranca",
                "description": "descricao da cobranca",
                "amount": {
                    "value": valor,
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "CREDIT_CARD",
                    "installments": kwargs.get('parcelas'),
                    "capture": True,
                    "card": {
                        "encrypted": kwargs.get('encrypted'),
                        "security_code": kwargs.get('cvv'),
                        "holder": {
                            "name": kwargs.get('holder')
                        },
                        "store": False
                    }
                }
            }
        ]
    }
    resposta = requests.post('https://sandbox.api.pagseguro.com/orders', json=body, headers=headers)
    print(resposta.text)
    print(kwargs.get('encrypted'))
    return resposta.json()
