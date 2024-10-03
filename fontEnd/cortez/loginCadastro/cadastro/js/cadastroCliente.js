btn.addEventListener("click", function(e){
    e.preventDefault()
    const email = document.getElementById("email").value
    const nome = document.getElementById("nome").value
    const cpf = document.getElementById("cpf").value
    const senha = document.getElementById("senha").value


    //cria um objeto com o nome do usuario e senha
    const cadastro = {
        "email": email,
        "nome": nome,
        "cpf": cpf,
        "senha": senha
    }

    //pega o objeto e transforma em JSON
    let obj = JSON.stringify(cadastro)
    console.log(obj)
})

function confereSenha(){
    if (senha1 == senha){
        senha1.setCustomValidity('')
    } else {
        senha1.setCustomValidity('Senhas Não Conferem')
    }
}