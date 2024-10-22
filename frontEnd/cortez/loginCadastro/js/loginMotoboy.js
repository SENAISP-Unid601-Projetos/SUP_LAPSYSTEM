btn.addEventListener("click", function(e) {
    e.preventDefault();
    const usuario = document.getElementById("usuario");
    const valorUsuario = usuario.value;
    const senha = document.getElementById("senha");
    const valorSenha = senha.value;

    const loginData = {
        "username": valorUsuario, 
        "password": valorSenha 
    };

    let obj = JSON.stringify(loginData);
    console.log(obj);

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
        console.log(data.message); 
        alert(data.message); 
        
        const motoboyId = data.motoboy_id;
        if (motoboyId) {
            localStorage.setItem('motoboyId', motoboyId);
        }

        window.location.href = "../../bruno/catalogo/index.html";    
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Falha ao realizar login.');
    });
});
