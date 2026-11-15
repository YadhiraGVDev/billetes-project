import cv2
import numpy as np


class AnalizadorCalidadBillete:
    def __init__(self):
        self.umbral_arruga = 0.015
        self.umbral_doblez = 0.03
        self.umbral_area_min = 0.85

    def analizar_desde_bytes(self, contenido: bytes) -> dict:
        """Recibe bytes de la imagen subida y devuelve el análisis."""
        array = np.frombuffer(contenido, np.uint8)
        imagen = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if imagen is None:
            return {
                "doblado": False, "arrugado": False, "roto": True,
                "puntaje_calidad": 0,
                "detalles": ["No se pudo decodificar la imagen"],
            }
        return self.analizar(imagen)

    def analizar(self, imagen_bgr):
        resultados = {
            "doblado": False,
            "arrugado": False,
            "roto": False,
            "puntaje_calidad": 100,
            "detalles": [],
        }

        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (5, 5), 0)

        arrugas_score = self._detectar_arrugas(gris)
        if arrugas_score > self.umbral_arruga:
            resultados["arrugado"] = True
            resultados["detalles"].append(
                f"Arrugas detectadas (score: {arrugas_score:.3f})"
            )

        doblez_score = self._detectar_dobleces(gris)
        if doblez_score > self.umbral_doblez:
            resultados["doblado"] = True
            resultados["detalles"].append(
                f"Dobleces detectados (score: {doblez_score:.3f})"
            )

        roto, rotura_score, motivo = self._detectar_roturas(imagen_bgr)
        if roto:
            resultados["roto"] = True
            resultados["detalles"].append(f"Billete roto: {motivo}")
        else:
            rotura_score = 0.0

        resultados["puntaje_calidad"] = max(
            0,
            100 - (arrugas_score * 500 + doblez_score * 400 + rotura_score * 600),
        )
        return resultados

    def _detectar_arrugas(self, gris):
        lap = cv2.Laplacian(gris, cv2.CV_64F)
        magnitud = np.abs(lap)
        media = magnitud.mean()
        umbral = np.percentile(magnitud, 95)
        pixeles_arruga = np.sum(magnitud > umbral) / magnitud.size
        return float(pixeles_arruga * (media / 255.0))

    def _detectar_dobleces(self, gris):
        bordes = cv2.Canny(gris, 50, 150)
        alto, ancho = gris.shape
        lineas = cv2.HoughLinesP(
            bordes, 1, np.pi / 180, threshold=80,
            minLineLength=int(ancho * 0.5), maxLineGap=10,
        )
        if lineas is None:
            return 0.0

        candidatas = 0
        margen = 10
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            largo = np.hypot(x2 - x1, y2 - y1)
            if (x1 < margen and x2 < margen) or (
                x1 > ancho - margen and x2 > ancho - margen
            ):
                continue
            if (y1 < margen and y2 < margen) or (
                y1 > alto - margen and y2 > alto - margen
            ):
                continue
            if largo > ancho * 0.5:
                candidatas += 1
        return min(1.0, candidatas * 0.03)

    def _detectar_roturas(self, imagen_bgr):
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        _, binaria = cv2.threshold(
            gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        contornos, _ = cv2.findContours(
            binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contornos:
            return True, 1.0, "sin contorno detectado"

        c = max(contornos, key=cv2.contourArea)
        area_real = cv2.contourArea(c)
        rect = cv2.minAreaRect(c)
        area_rect = rect[1][0] * rect[1][1]
        if area_rect == 0:
            return True, 1.0, "billete ilegible"

        ratio = area_real / area_rect
        if ratio < self.umbral_area_min:
            return True, (1 - ratio), f"borde irregular (ratio {ratio:.2f})"

        contornos_int, jerarquia = cv2.findContours(
            binaria, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        agujeros = 0
        if jerarquia is not None:
            for i, h in enumerate(jerarquia[0]):
                if h[3] != -1 and cv2.contourArea(contornos_int[i]) > (
                    area_real * 0.002
                ):
                    agujeros += 1
        if agujeros > 0:
            return True, min(1.0, agujeros * 0.15), f"{agujeros} agujero(s)"

        return False, 0.0, "ok"