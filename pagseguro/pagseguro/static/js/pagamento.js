
function gerarCard() {
    var card = PagSeguro.encryptCard({
      publicKey: document.querySelector('#key').value,
      holder: document.querySelector('#holder').value,
      number: document.querySelector('#ncartao').value,
      expMonth: document.querySelector('#mesvencimento').value,
      expYear: document.querySelector('#anovencimento').value,
      securityCode: document.querySelector('#cvv').value
    });
    var encrypted = card;
    return encrypted
    }


function get_crypt() {
    var cardones = gerarCard()
    var encrypt = ''
    if (cardones.hasErrors) {
    for (let index = 0; index < cardones.errors.length; index++) {
        encrypt += cardones.errors[index].message + '\n'
    }
}
    else {
        encrypt = cardones.encryptedCard
    }
    var inputOculto = document.createElement('input');
    inputOculto.type = 'hidden';
    inputOculto.name = 'encrypted';
    inputOculto.value = encrypt;

    // Adicionar o input oculto a um formulário existente
    var formulario = document.getElementById('card');
    formulario.appendChild(inputOculto);

    return encrypt
 }
