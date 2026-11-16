document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const captureBtn = document.getElementById("capture-btn");
    const switchBtn = document.getElementById("switch-camera-btn");
    const fileInput = document.getElementById("file-input");

    let stream = null;
    let facingMode = "environment";
    let iniciando = false;

    if (!video || !canvas || !captureBtn || !switchBtn || !fileInput) {
        console.error("No se encontraron todos los elementos de la cámara.");
        return;
    }

    video.setAttribute("autoplay", "");
    video.setAttribute("playsinline", "");
    video.setAttribute("muted", "");
    video.muted = true;

    async function startCamera() {
        if (iniciando) return;

        if (!navigator.mediaDevices?.getUserMedia) {
            alert("Tu navegador no permite acceder a la cámara. Comprueba que utilizas HTTPS y Chrome.");
            return;
        }

        if (!window.isSecureContext) {
            alert("La cámara necesita una conexión segura HTTPS.");
            return;
        }

        iniciando = true;
        captureBtn.disabled = true;

        try {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }

            const constraints = {
                audio: false,
                video: {
                    facingMode: { ideal: facingMode },
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            };

            stream = await navigator.mediaDevices.getUserMedia(constraints);

            const metadataPromise = new Promise((resolve, reject) => {
                video.addEventListener("loadedmetadata", resolve, { once: true });
                video.addEventListener("error", reject, { once: true });
            });

            video.srcObject = stream;

            if (video.readyState < 1) {
                await metadataPromise;
            }

            await video.play();

            console.log("Cámara iniciada correctamente.");
            console.log("Resolución:", video.videoWidth, "x", video.videoHeight);

        } catch (err) {
            console.error("Error al iniciar cámara:", err);

            const errores = {
                NotAllowedError: "El navegador no permite utilizar la cámara. Revisa los permisos.",
                PermissionDeniedError: "El acceso a la cámara fue rechazado.",
                NotFoundError: "No se encontró una cámara disponible.",
                NotReadableError: "La cámara está siendo utilizada por otra aplicación.",
                OverconstrainedError: "La cámara no admite la configuración solicitada.",
                AbortError: "La cámara dejó de funcionar. Intenta nuevamente."
            };

            alert(errores[err.name] || "No se pudo iniciar la cámara: " + err.message);

        } finally {
            iniciando = false;
            captureBtn.disabled = false;
        }
    }

    startCamera();

    switchBtn.addEventListener("click", async () => {
        facingMode = facingMode === "environment" ? "user" : "environment";
        await startCamera();
    });

    captureBtn.addEventListener("click", async () => {
        if (!stream || video.readyState < 2 || !video.videoWidth) {
            alert("La cámara todavía no está lista. Espera unos segundos.");
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext("2d");

        if (!context) {
            alert("No se pudo preparar la fotografía.");
            return;
        }

        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // CAMBIO 1: Bajamos la calidad a 0.7 para que pese menos y no sature el localStorage en móviles
        const imageData = canvas.toDataURL("image/jpeg", 0.7);
        
        guardarYIrAPreview(imageData);
    });

    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];

        if (!file) return;

        if (!file.type.startsWith("image/")) {
            alert("Selecciona un archivo de imagen válido.");
            return;
        }

        const reader = new FileReader();

        reader.onload = (event) => {
            guardarYIrAPreview(event.target.result);
        };

        reader.onerror = () => {
            alert("No se pudo leer la imagen seleccionada.");
        };

        reader.readAsDataURL(file);
    });

    function guardarYIrAPreview(base64Image) {
        try {
            localStorage.setItem("fotoBillete", base64Image);
            
            // CAMBIO 2: Usamos una ruta relativa simple. 
            // Si tu URL en Django es '/preview/', esto funcionará perfecto.
            window.location.href = "/preview/"; 
            
        } catch (error) {
            console.error("Error al guardar fotografía:", error);
            // Este error suele pasar si la foto es muy grande para el almacenamiento del móvil
            alert("La fotografía es muy pesada para procesarla. Intenta de nuevo o usa la galería.");
        }
    }

    window.addEventListener("pagehide", () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    });
});