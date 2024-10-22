btn.addEventListener("click", function(e) {
    e.preventDefault();
    
    const email = document.getElementById("email").value; 
    const username = document.getElementById("nome").value; 
    const cpf = document.getElementById("cpf").value; 
    const senha = document.getElementById("senha").value; 
    const senha1 = document.getElementById("senha1").value; 
   

    const fotoRosto = document.getElementById("fotoRosto").files[0];
    const cnh = document.getElementById("cnh").files[0];
    const fotoMoto = document.getElementById("fotoMoto").files[0];
    const documentoMoto = document.getElementById("documentoMoto").files[0];

    if (senha !== senha1) {
        alert("Senhas não conferem"); 
        return; 
    }

    const cadastro = {
        "email": email,
        "username": username, 
        "cpf": cpf,
        "password": senha, 
    };

    const formData = new FormData();
    formData.append("cadastro", JSON.stringify(cadastro)); 
    formData.append("file1", fotoRosto);
    formData.append("file2", cnh);
    formData.append("file3", fotoMoto);
    formData.append("file4", documentoMoto);

    fetch('http://127.0.0.1:5000/motoboys/register', {  
        method: 'POST',
        body: formData 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao cadastrar motoboy: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message); 
        alert(data.message); 
        window.location.href = "loginMotoboy.html"; 
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Falha ao cadastrar motoboy.');
    });
});
