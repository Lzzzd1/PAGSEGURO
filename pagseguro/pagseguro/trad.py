from flask import Blueprint, render_template, request
from integracao.requisition import get_key, gerar_boleto, gerar_pix, gerar_cartao
from forms import ClienteForm, EnderecoForm
from pagseguro.integracao.utils import calcular_juros, calcular_parcelas

trad = Blueprint('trad', __name__)


@trad.route('/')
def index():
    cli_form = ClienteForm()
    end_form = EnderecoForm()
    key = get_key()
    valor = 697
    plano = 'Tradicional'
    parcelas = [calcular_parcelas(calcular_juros(697, i), i) for i in range(1, 13)]
    return render_template('link.html', cli_form=cli_form, end_form=end_form, key=key, valor=valor, plano=plano,
                           parcelas=parcelas)


# @api.post('/teste')
# def tok():
#     form = ClienteForm()
#     if form.validate_on_submit():
#         for i in form:
#             session[i.name] = i.data
#             print(session[i.name])
#     return 'ai'


@trad.post('/boleto')
def boleto():
    boleto = gerar_boleto(69700, **request.form.to_dict())
    return boleto['charges'][0]['links'][0]['href']


@trad.post('/pix')
def pix():
    pix = gerar_pix(69700, **request.form.to_dict())
    codigo = pix['qr_codes'][0]['text']
    qr_code = pix['qr_codes'][0]['links'][0]['href']
    print(codigo, '\n', qr_code)
    return {'codigo': codigo, 'qr_code': qr_code}


@trad.post('/cartao')
def cartao():
    cartao = gerar_cartao(69700, **request.form.to_dict())
    return cartao

def configure(app):
    app.register_blueprint(trad, url_prefix='/trad')
