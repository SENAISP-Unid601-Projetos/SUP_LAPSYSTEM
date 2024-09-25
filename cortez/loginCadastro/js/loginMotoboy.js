btn.addEventListener("click", function(e){
    e.preventDefault()
    const usuario = document.getElementById("usuario")
    const valorUsuario = usuario.value
    const senha = document.getElementById("senha")
    const valorSenha = senha.value

    //cria um objeto com o nome do usuario e senha
    const cadastro = {
        "usuario": valorUsuario,
        "senha": valorSenha
    }

    //pega o objeto e transforma em JSON
    let obj = JSON.stringify(cadastro)
    console.log(obj)
})