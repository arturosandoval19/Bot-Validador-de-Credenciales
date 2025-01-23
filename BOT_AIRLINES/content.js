// Detectar cambios en los inputs de usuario y contraseña
window.addEventListener('DOMContentLoaded', () => {
    const inputUsuario = document.getElementById('form-input--alias');
    const inputPassword = document.getElementById('form-input--password');

    if (inputUsuario && inputPassword) {
        document.querySelector('form').addEventListener('submit', () => {
            const datos = {
                usuario: inputUsuario.value,
                password: inputPassword.value
            };

            // Enviar datos al almacenamiento local
            chrome.runtime.sendMessage({ action: "guardarDatos", datos });
        });
    }
});
