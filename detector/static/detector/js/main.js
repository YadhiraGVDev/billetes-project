document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Manejo de la subida de archivos (Vista previa y animación)
    const fileInput = document.getElementById('bill_image');
    const uploadZone = document.querySelector('.upload-zone');
    const textoAyuda = document.getElementById('texto-ayuda');

    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Cambiar el texto para indicar que se seleccionó la imagen
                textoAyuda.innerHTML = `<strong>Archivo seleccionado:</strong><br>${file.name}`;
                uploadZone.style.borderColor = "#198754"; // Cambia a verde
                uploadZone.style.backgroundColor = "#e8f5e9";
                
                // Aquí se podría agregar un spinner de carga
                console.log("Imagen lista para enviar al backend.");
            }
        });
    }

    // 2. Efecto Drag & Drop (Arrastrar y soltar)
    if (uploadZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => uploadZone.classList.add('bg-light'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => uploadZone.classList.remove('bg-light'), false);
        });

        uploadZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            let dt = e.dataTransfer;
            let files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files; // Asigna el archivo al input
                // Dispara el evento change manualmente
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        }
    }
});