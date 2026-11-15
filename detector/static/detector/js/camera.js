document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('capture-btn');
    const switchBtn = document.getElementById('switch-camera-btn');
    const fileInput = document.getElementById('file-input');

    let stream = null;
    let facingMode = "environment"; // "environment" es la cámara trasera

    // Función para iniciar la cámara
    async function startCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop()); // Apagar cámara anterior
        }

        const constraints = {
            video: { facingMode: facingMode }
        };

        try {
            stream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = stream;
        } catch (err) {
            console.error("Error al acceder a la cámara: ", err);
            alert("No se pudo acceder a la cámara. Asegúrate de dar permisos.");
        }
    }

    // Iniciar cámara al cargar
    startCamera();

    // Cambiar cámara (frontal/trasera)
    switchBtn.addEventListener('click', () => {
        facingMode = facingMode === "environment" ? "user" : "environment";
        startCamera();
    });

    // Tomar foto
    captureBtn.addEventListener('click', () => {
        // Ajustar el canvas al tamaño del video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Dibujar el frame actual del video en el canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convertir a imagen
        const imageData = canvas.toDataURL('image/jpeg', 0.8); // 0.8 es la calidad

        // Ir a la vista previa
        guardarYIrAPreview(imageData);
    });

    // Subir desde galería
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                guardarYIrAPreview(event.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // =========================================================
    // FUNCIÓN QUE GUARDA LA IMAGEN Y REDIRIGE A LA VISTA PREVIA
    // =========================================================
    function guardarYIrAPreview(base64Image) {
        // 1. Guardamos la foto en el almacenamiento local del navegador
        localStorage.setItem('fotoBillete', base64Image);
        
        // 2. Redirigimos a la nueva pantalla de vista previa
        window.location.href = "/preview/"; 
    }

});