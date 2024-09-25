btn.addEventListener("click", function(e){
    e.preventDefault()
    const email = document.getElementById("email").value   //pega valor do email e guarda em uma variavel
    const nome = document.getElementById("nome").value     //pega valor do nome e guarda em uma variavel
    const cpf = document.getElementById("cpf").value       //pega valor do cpf e guarda em uma variavel
    const senha = document.getElementById("senha").value   //pega valor do senha e guarda em uma variavel
    const senha1 = document.getElementById("senha1").value //pega valor do senha e guarda em uma variavel

    if(senha != senha1){
        document.alert("senha invalida")
    }

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