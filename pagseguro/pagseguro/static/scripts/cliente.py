from browser import document, bind, window
from browser.html import SMALL, SPAN, H3, IMG, DIV, BUTTON, BR, P
from browser import ajax
from browser.timer import set_timeout
import re


def on_complete(req):
    print(req.status)


def validar_campos(campos):
    if not all(i.value for i in campos):
        erros = document.select('.erro')
        if erros:
            for p in erros:
                p.remove()
        for campo in campos:
            
            campo.style.borderColor = '#0854fe'
            if not campo.value:
                campo.style.borderColor = 'red'
                # noinspection PyStatementEffect
                campo.parent <= DIV( BR() + SMALL(
                    f'O campo ' + SPAN(campo.placeholder.lower(), style={"color": "red"}) + ' é obrigatório',
                    style={"color": "white"}), Class = "erro" )
        return False
    # valores = [{'nome': i.id, 'valor': i.value} for i in campos]
    # for dados in valores:
    #     print(dados)
    #     ajax.post('/receber', data=dados)
    return True


def on_completar_envio(req):
    # Função de retorno chamada quando o envio do formulário é concluído
    if req.status == 200:
        # Envio bem-sucedido
        print("Formulário enviado com sucesso!")
    else:
        # Envio falhou
        print("Erro ao enviar o formulário.")


@bind(document['cliente'], 'click')
def cli(evt):
    campos = document.select('.cliente input:not([type="submmit"])')

    if not validar_campos(campos):
        return None

    # dados = dict()
    # for campo in campos:
    #     dados[campo.name] = campo.value
    # ajax.post('/teste', data=dados, oncomplete=on_completar_envio)

    document.select_one('.cliente').hidden = True
    document.select_one('.endereco').hidden = False
    document['clii'].class_name = 'bx bx-check-circle'
    evt.currentTarget.id = 'end'

    @bind(document['end'], 'click')
    def endo(evt):
        campos = document.select('.endereco input')
        if not validar_campos(campos):
            return None
        document['endi'].class_name = 'bx bx-check-circle'
        document.select_one('.endereco').hidden = True
        evt.currentTarget.hidden = True
        document['cartao'].hidden = False
        document['boleto'].hidden = False
        document['pix'].hidden = False
        document.select_one('.pagamento_cartao').hidden = False


@bind(document['cpf'], 'input')
def validar_cpf(evt):
    cpf = evt.currentTarget.value
    if p := evt.currentTarget.parent.parent.select_one('small'):
        p.remove()
    # Verifica a formatação do CPF
    if not re.match(r'\d{3}.?\d{3}.?\d{3}-?\d{2}', cpf):
        evt.currentTarget.parent.parent <= SMALL('CPF inválido', style={"color": "red"})
        document['cliente'].disabled = True
        return None

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        evt.currentTarget.parent.parent <= SMALL('CPF inválido', style={"color": "red"})
        document['cliente'].disabled = True
        return None
    document['cliente'].disabled = False
    # evt.currentTarget.parent.select_one('small').remove()


@bind(document['email'], 'input')
def validar_email(evt):
    email = evt.currentTarget.value
    if p := evt.currentTarget.parent.parent.select_one('small'):
        p.remove()
    if not re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        evt.currentTarget.parent.parent <= SMALL('Email inválido', style={"color": "red"})
        document['cliente'].disabled = True
        return None
    document['cliente'].disabled = False


@bind(document['telefone'], 'input')
def validar_telefone(evt):
    telefone = evt.currentTarget.value
    if p := evt.currentTarget.parent.parent.select_one('small'):
        p.remove()
    if not re.match(
            r'^(55)?\(?(?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$',
            telefone):
        evt.currentTarget.parent.parent <= SMALL('Telefone inválido', style={"color": "red"})
        document['cliente'].disabled = True
        return None
    document['cliente'].disabled = False


@bind(document['boleto'], 'click')
def boleto(evt):
    document.select_one('.pagamento_cartao').hidden = True
    document.select_one('.pagamento_pix').hidden = True
    document.select_one('.pagamento_boleto').hidden = False


@bind(document['pix'], 'click')
def pix(evt):
    document.select_one('.pagamento_cartao').hidden = True
    document.select_one('.pagamento_pix').hidden = False
    document.select_one('.pagamento_boleto').hidden = True


@bind(document['bboleto'], 'click')
def gerar_boleto(evt):
    inputs = document.select('input:not([type="button"])')
    document.select_one('.avisob').hidden = True
    document['carregarb'].hidden = False
    dados = dict()
    for input in inputs:
        dados[input.name] = input.value
    ajax.post(window.location.href + '/boleto', data=dados, oncomplete=acessar)


@bind(document['bpix'], 'click')
def gerar_pix(evt):
    inputs = document.select('input:not([type="button"])')
    document.select_one('.aviso').hidden = True
    document['carregar'].hidden = False
    dados = dict()
    for input in inputs:
        dados[input.name] = input.value
    ajax.post(window.location.href + '/pix', data=dados, oncomplete=link_e_imagem)
    evt.currentTarget.hidden = True


@bind(document['bcartao'], 'click')
def gerar_cartao(evt):
    inputs = filter(lambda x: x.Type not in ['button', 'submit'], document.select('input'))
    if not validar_campos(inputs):
        return False
    resposta = window.get_crypt()
    if not resposta.endswith('=='):
        div = document.select_one('.menus')
        for z, i in enumerate(resposta.splitlines(0)):
            div <= P(i, style={'color': 'red', 'padding-top': '5%'}, Class=f'erro')
        set_timeout(lambda: [erro.remove() for erro in document.select('.erro')], 7000)
        return None

    evt.currentTarget.hidden = True
    document['carregarc'].hidden = False
    inputs = filter(lambda x: x.type not in ['button', 'submit'], document.select('input'))
    dados = dict()
    for input in inputs:
        dados[input.name] = input.value
    dados['parcelas'] = document['parcelas'].value
    ajax.post(window.location.href + '/cartao', data=dados, oncomplete=testar)


def testar(req):
    document['carregarc'].hidden = True
    document['bcartao'].hidden = False
    resposta = req.json
    div = document.select_one('.menus')
    try:
        if resposta['charges'][0]['status'] == 'PAID':
            document.select_one('.col-lg-10').hidden = True
            document.select_one('.sucesso').hidden = False
            document['pagi'].class_name = 'bx bx-check-circle'
        else:
            print(resposta['charges'][0]['status'])
            raise Exception()
    except Exception as e:
        div <= P('Pagamento recusado!', style={'color': 'red', 'padding-top': '5%'}, Id='recusado')
        set_timeout(lambda: document['recusado'].remove(), 5000)
        return 0









@bind(document['cartao'], 'click')
def cartao(evt):
    document.select_one('.pagamento_cartao').hidden = False
    document.select_one('.pagamento_pix').hidden = True
    document.select_one('.pagamento_boleto').hidden = True


def acessar(req):
    document['carregarb'].hidden = True
    window.location.href = req.text
    document.select_one('.avisob').hidden = False


def link_e_imagem(req):
    resposta = req.json
    document['carregar'].hidden = True
    div = document.select_one('.pagamento_pix')
    div <= H3('Pix copia e cola', style={'color': '#089ff4'})
    div <= SMALL(resposta['codigo'], style={'color': 'white'}, Id='codigo')
    div <= DIV(BUTTON('Copiar', Id='copiar', Type='submit', style={
        'margin-top': '5%',
        'margin-bottom': '2%',
        'width': '50%',
        'background': 'var(--bs-blue)',
    }), style={'text-align': 'center'})
    document['copiar'].bind('click', copiar)
    div <= DIV(IMG('QR Code', src=resposta['qr_code'],
                   style={'width': '150px', 'height': '150px'}),
               style={'margin-top': '3%'})


def copiar(evt):
    cod = document['codigo'].text
    window.navigator.clipboard.writeText(cod)
    evt.currentTarget.innerText = 'Copiado!'
    set_timeout(mudar_texto, 3000)


def mudar_texto():
    document['copiar'].innerText = 'Copiar'

# def endo(evt):
#     document.select_one('.endereco').hidden = True
#     document.select_one('.pagemento cartao').hidden = False
#     evt.currentTarget.id = 'end'