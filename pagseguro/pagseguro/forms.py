from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, IntegerField
from wtforms.validators import Length


class ClienteForm(FlaskForm):
    nome = StringField('Nome Completo')
    cpf = StringField('CPF')
    email = EmailField('Email')
    telefone = TelField('Telefone')


class EnderecoForm(FlaskForm):
    cep = StringField('CEP', validators=[Length(max=9)])
    uf = StringField('UF')
    cidade = StringField('Cidade')
    bairro = StringField('Bairro')
    endereco = StringField('Endereço')
    numero = StringField('Numero')
    complemento = StringField('Complemento')

