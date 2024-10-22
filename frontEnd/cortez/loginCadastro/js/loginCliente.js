btn.addEventListener("click", function(e) {
    e.preventDefault();
    const usuario = document.getElementById("usuario");
    const valorUsuario = usuario.value;
    const senha = document.getElementById("senha");
    const valorSenha = senha.value;

    // Cria um objeto com o nome do usuário e senha
    const loginData = {
        "username": valorUsuario, // Atualizado para "username" para corresponder ao endpoint
        "password": valorSenha // Atualizado para "password" para corresponder ao endpoint
    };

    // Transforma o objeto em JSON
    let obj = JSON.stringify(loginData);
    console.log(obj);

    // Envia os dados para o servidor
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: obj
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao realizar login: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message); // Mensagem de sucesso
        alert(data.message); // Exibe a mensagem ao usuário
        // Aqui você pode redirecionar o usuário ou armazenar informações no localStorage
        window.location.href = "../../bruno/catalogo/index.html"    


    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Falha ao realizar login.');
    });
});
