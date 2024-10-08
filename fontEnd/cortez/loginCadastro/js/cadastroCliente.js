btn.addEventListener("click", function(e) {
    e.preventDefault();
    
    const email = document.getElementById("email").value;
    const username = document.getElementById("nome").value; // Alterado para "username"
    const cpf = document.getElementById("cpf").value;
    const senha = document.getElementById("senha").value;

    // Cria um objeto com os dados do usuário
    const cadastro = {
        "email": email,
        "username": username, // Agora é "username"
        "cpf": cpf,
        "password": senha // Renomeado para "password" para corresponder ao endpoint
    };

    // Transforma o objeto em JSON
    let obj = JSON.stringify(cadastro);
    console.log(obj);

    // Envia os dados para o servidor
    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: obj
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao cadastrar usuário: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message); // Mensagem de sucesso
        alert(data.message); // Exibe a mensagem ao usuário
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Falha ao cadastrar usuário.');
    });
});

function confereSenha() {
    const senha1 = document.getElementById("senha1"); // Assumindo que você tem um campo para confirmar a senha
    const senha = document.getElementById("senha").value;
    
    if (senha1.value === senha) {
        senha1.setCustomValidity('');
    } else {
        senha1.setCustomValidity('Senhas Não Conferem');
    }
}
