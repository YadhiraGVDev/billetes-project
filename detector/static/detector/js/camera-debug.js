document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');

    const estado = document.createElement('div');
    estado.style.cssText = 'position:fixed;top:10px;left:10px;right:10px;z-index:999999;background:white;color:black;padding:15px;border:3px solid red;font-size:15px;';
    document.body.appendChild(estado);

    const mostrar = mensaje => {
        estado.textContent = mensaje;
        console.log('[CAMARA]', mensaje);
    };

    mostrar('1. JavaScript cargado');

    if (!video) {
        mostrar('ERROR: No se encontró el video');
        return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
        mostrar('ERROR: getUserMedia no está disponible');
        return;
    }

    try {
        mostrar('2. Solicitando cámara...');

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { facingMode: { ideal: 'environment' } }
        });

        mostrar('3. Cámara detectada');

        video.srcObject = stream;
        video.muted = true;
        video.playsInline = true;

        await video.play();

        mostrar('4. CÁMARA FUNCIONANDO: ' + video.videoWidth + ' x ' + video.videoHeight);

    } catch (error) {
        mostrar('ERROR: ' + error.name + ' - ' + error.message);
    }
});
