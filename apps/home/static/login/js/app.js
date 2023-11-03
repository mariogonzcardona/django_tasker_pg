// Process to login
document.getElementById("btnLogin").addEventListener("click", login);

async function login() {
    const username = document.getElementById('inputUsername').value;
    const password = document.getElementById('inputPass').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log(username, password, csrftoken);

    fetch('/api/v1/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            email: username,
            password: password
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Credenciales incorrectas');
            }
            return response.json();
        })
        .then(data => {
            if (data.access) {
                // Almacenar el token JWT en localStorage
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);

                Swal.fire({
                    title: `Bienvenido ${data.full_name}!`,
                    icon: 'success',
                    showConfirmButton: false,
                    timer: 1500
                });
                setTimeout(function () {
                    window.location.href = "/";
                }, 1500);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Error al iniciar sesión, intente de nuevo.',
                icon: 'error',
                showConfirmButton: true
            });
        });
}