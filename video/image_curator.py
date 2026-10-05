"""
Módulo de Curaduría y Normalización de Imágenes Fotográficas.
Filtra estrictamente imágenes reales, documentales y de archivo histórico,
descartando dibujos, caricaturas, vectores e ilustraciones.
Asegura resolución profesional nativa 1920x1080 (16:9).
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Optional, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np


class ImageCurator:
    """Busca, filtra, descarga y normaliza fotografías documentales para video."""

    def __init__(self, cache_dir: str = "temp/video_assets"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

        # Palabras prohibidas para evitar dibujos, vectores, grabados o caricaturas
        self.forbidden_keywords = {
            "cartoon", "clipart", "illustration", "vector", "drawing",
            "caricature", "sketch", "comic", "anime", "painting", "render",
            "engraving", "woodcut", "etching", "diagram", "lithograph", "map", "chart"
        }

    def fetch_scene_images(self, scene: Dict[str, Any], count: int = 3) -> List[str]:
        """Obtiene múltiples fotografías documentales reales para una escena (montaje dinámico multi-toma)."""
        search_terms = scene.get("search_terms", ["historical documentary photo"])
        images = []
        found_urls = set()

        # Intentar obtener fotografías reales distintas para la escena
        for term in search_terms:
            if len(images) >= count:
                break
            try:
                candidate_urls = self._search_wikimedia_commons_multi(term, limit=6)
                for url in candidate_urls:
                    if url in found_urls:
                        continue
                    found_urls.add(url)
                    idx = len(images)
                    raw_temp = os.path.join(self.cache_dir, f"raw_{scene['scene_index']}_{idx}.jpg")
                    out_path = os.path.join(self.cache_dir, f"scene_{scene['scene_index']}_shot_{idx}.jpg")
                    if self._download_file(url, raw_temp):
                        self.normalize_to_1080p(raw_temp, out_path, scene=scene, bake_overlay=False)
                        images.append(out_path)
                        if len(images) >= count:
                            break
            except Exception:
                continue

        # Si faltan imágenes para completar la cuota, complementar con lámina fotodocumental institucional
        while len(images) < count:
            idx = len(images)
            plate_out = os.path.join(self.cache_dir, f"scene_{scene['scene_index']}_plate_{idx}.jpg")
            self.generate_editorial_plate(scene, plate_out)
            images.append(plate_out)

        return images

    def fetch_scene_image(self, scene: Dict[str, Any], output_path: str) -> str:
        """Obtiene una imagen fotográfica principal para la escena (compatibilidad hacia atrás)."""
        imgs = self.fetch_scene_images(scene, count=1)
        if imgs and imgs[0] != output_path:
            shutil.copy2(imgs[0], output_path)
            return output_path
        return imgs[0] if imgs else output_path

    def _search_wikimedia_commons_multi(self, query: str, limit: int = 6) -> List[str]:
        """Busca y retorna múltiples URLs de fotografías reales descartando dibujos, vectores, grabados o PDFs."""
        clean_query = query.replace("documentary photography", "").replace("historical archive photo", "").strip()
        search_term = f"{clean_query} filetype:bitmap -drawing -vector -cartoon -clipart -pdf -engraving -woodcut -etching -diagram -map"
        encoded = urllib.parse.quote(search_term)
        url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
            f"&gsrsearch={encoded}&gsrnamespace=6&gsrlimit={limit * 2}"
            f"&prop=imageinfo&iiprop=url|mime|size&format=json"
        )
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BrainPoliticsVideoBot/1.0 (contact: info@ades.cloud)"}
        )

        results = []
        try:
            with urllib.request.urlopen(req, timeout=6) as response:
                data = json.loads(response.read().decode("utf-8"))

            pages = data.get("query", {}).get("pages", {})
            for _, page in pages.items():
                title = page.get("title", "").lower()
                if any(forbidden in title for forbidden in self.forbidden_keywords):
                    continue

                imageinfo = page.get("imageinfo", [])
                if not imageinfo:
                    continue

                info = imageinfo[0]
                mime = info.get("mime", "").lower()
                width = info.get("width", 0)
                height = info.get("height", 0)

                if mime in ["image/jpeg", "image/png"] and width >= 650 and height >= 400:
                    if not any(ext in title for ext in [".svg", ".gif", ".webp", ".pdf"]):
                        results.append(info.get("url"))
                        if len(results) >= limit:
                            break
        except Exception:
            pass

        return results

    def _search_wikimedia_commons(self, query: str) -> Optional[str]:
        """Busca una imagen única en Wikimedia Commons."""
        res = self._search_wikimedia_commons_multi(query, limit=1)
        return res[0] if res else None

    def _download_file(self, url: str, target_path: str) -> bool:
        """Descarga un archivo remoto con cabeceras de navegador respetuosas."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BrainPoliticsVideoBot/1.0 (contact: info@ades.cloud)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp, open(target_path, "wb") as out:
                out.write(resp.read())
            with Image.open(target_path) as img:
                img.verify()
            return True
        except Exception:
            if os.path.exists(target_path):
                os.remove(target_path)
            return False

    def normalize_to_1080p(
        self,
        input_path: str,
        output_path: str,
        scene: Optional[Dict[str, Any]] = None,
        bake_overlay: bool = False
    ) -> str:
        """Normaliza cualquier imagen a 1920x1080 (16:9) nativo de alta resolución.
        
        Si la relación de aspecto no es 16:9, preserva la fotografía completa centrada
        sobre un fondo cinematográfico sutilmente desenfocado y oscurecido.
        """
        target_w, target_h = 1920, 1080

        with Image.open(input_path) as img:
            img = img.convert("RGB")
            orig_w, orig_h = img.size
            aspect = orig_w / float(orig_h)
            target_aspect = target_w / float(target_h)

            if abs(aspect - target_aspect) < 0.08:
                scale = max(target_w / orig_w, target_h / orig_h)
                new_w, new_h = int(orig_w * scale), int(orig_h * scale)
                resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                left = (new_w - target_w) // 2
                top = (new_h - target_h) // 2
                final_img = resized.crop((left, top, left + target_w, top + target_h))
            else:
                bg_scale = max(target_w / orig_w, target_h / orig_h)
                bg_w, bg_h = int(orig_w * bg_scale), int(orig_h * bg_scale)
                bg = img.resize((bg_w, bg_h), Image.Resampling.BILINEAR)
                bg_left = (bg_w - target_w) // 2
                bg_top = (bg_h - target_h) // 2
                bg_cropped = bg.crop((bg_left, bg_top, bg_left + target_w, bg_top + target_h))
                bg_blurred = bg_cropped.filter(ImageFilter.GaussianBlur(radius=28))
                enhancer = ImageEnhance.Brightness(bg_blurred)
                bg_dark = enhancer.enhance(0.40)

                fg_scale = min(target_w / orig_w, target_h / orig_h) * 0.94
                fg_w, fg_h = int(orig_w * fg_scale), int(orig_h * fg_scale)
                fg_resized = img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

                paste_x = (target_w - fg_w) // 2
                paste_y = (target_h - fg_h) // 2
                final_img = bg_dark.copy()
                final_img.paste(fg_resized, (paste_x, paste_y))

            if bake_overlay and scene:
                overlay_tmp = os.path.join(self.cache_dir, "temp_ov.png")
                self.create_lower_third_overlay(scene, overlay_tmp)
                with Image.open(overlay_tmp) as ov:
                    final_img = Image.alpha_composite(final_img.convert("RGBA"), ov).convert("RGB")
                if os.path.exists(overlay_tmp):
                    os.remove(overlay_tmp)

            final_img.save(output_path, "JPEG", quality=95)

        return output_path

    def create_lower_third_overlay(self, scene: Dict[str, Any], output_path: str) -> str:
        """Genera una capa gráfica transparente PNG (1920x1080) con el zócalo documental de ADES.CLOUD.
        
        Diseño profesional de televisión y cine documental:
        - Scrim cinemático con degradado de opacidad (y=720 a 1080)
        - Línea de acento carmesí (#b22222) institucional
        - Título temático limpio y envolvente sin cortes de palabras (hasta 2 líneas, Helvetica 30)
        - Cita o síntesis conceptual destacada (hasta 2 líneas, Helvetica 22)
        - Sello institucional 'ADES.CLOUD | INVESTIGACIÓN' en la esquina inferior derecha
        - Se superpone ESTÁTICAMENTE en el video para que el zoom/paneo de cámara nunca corte el texto.
        """
        target_w, target_h = 1920, 1080
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # 1. Scrim cinemático: degradado suave de y=670 a y=745, y fondo sólido de y=745 a y=1080
        ramp_start = 670
        ramp_end = 745
        ramp_h = ramp_end - ramp_start
        alpha_ramp = np.linspace(0, 235, ramp_h).astype(np.uint8)
        for i, alpha in enumerate(alpha_ramp):
            y_pos = ramp_start + i
            draw_ov.line([(0, y_pos), (target_w, y_pos)], fill=(8, 12, 16, int(alpha)))

        # Fondo sólido oscuro desde y=745 hasta 1080 para legibilidad absoluta
        draw_ov.rectangle([(0, ramp_end), (target_w, target_h)], fill=(8, 12, 16, 235))

        # 2. Línea de acento institucional superior
        draw_ov.rectangle([(0, 744), (target_w, 747)], fill=(178, 34, 34, 255))
        draw_ov.rectangle([(80, 743), (320, 748)], fill=(225, 45, 45, 255))

        # 3. Tipografía del sistema
        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 30)
            font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 21)
            font_badge = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 19)
        except Exception:
            font_title = ImageFont.load_default()
            font_sub = font_title
            font_badge = font_title

        # 4. Título sin cortes (envolvente en hasta 2 líneas fluidas)
        title_txt = scene.get("title", "")
        title_lines = self._wrap_text(title_txt, max_chars=60)[:2]

        curr_y = 765
        for line in title_lines:
            draw_ov.text((80, curr_y), line, fill=(255, 255, 255, 255), font=font_title)
            curr_y += 38

        # 5. Cita o síntesis destacada sin cortes
        quote_txt = scene.get("overlay_quote", "")
        if quote_txt and quote_txt != title_txt:
            clean_q = quote_txt.strip().strip("«»\"'")
            quote_lines = self._wrap_text(f"«{clean_q}»", max_chars=68)
            if len(quote_lines) > 2:
                line1 = quote_lines[1].rstrip(" .,;:-")
                if line1.endswith("»"):
                    line1 = line1[:-1]
                quote_lines = [quote_lines[0], f"{line1}...»"]

            curr_y += 6
            for ql in quote_lines:
                draw_ov.text((80, curr_y), ql, fill=(210, 222, 238, 245), font=font_sub)
                curr_y += 28

        # 6. Sello institucional en esquina inferior derecha
        draw_ov.text((1440, 1020), "ADES.CLOUD | INVESTIGACIÓN", fill=(185, 195, 210, 230), font=font_badge)

        overlay.save(output_path, "PNG")
        return output_path

    def generate_editorial_plate(self, scene: Dict[str, Any], output_path: str) -> str:
        """Genera una lámina editorial cinematográfica de alta definición con estética de ADES.CLOUD.
        
        Utiliza un degradado textural oscuro (#0d1117 a #161b22), viñeteado y tipografía sobria.
        """
        w, h = 1920, 1080
        # Crear gradiente base oscuro mediante NumPy
        y = np.linspace(0, 1, h)[:, None]
        x = np.linspace(0, 1, w)[None, :]
        
        # Color primario: oscuro institucional (#12161c a #1b2028)
        r = (18 + 12 * (1 - y) + 5 * x).astype(np.uint8)
        g = (22 + 10 * (1 - y) + 4 * x).astype(np.uint8)
        b = (28 + 14 * (1 - y) + 8 * x).astype(np.uint8)
        rgb_array = np.dstack((r, g, b))

        img = Image.fromarray(rgb_array, mode="RGB")
        draw = ImageDraw.Draw(img, "RGBA")

        # Dibujar líneas guía sutiles y viñeteado
        accent_color = (178, 34, 34, 255)       # Carmesí ADES
        subtle_line = (80, 90, 105, 120)

        # Barra superior institucional
        draw.rectangle([(80, 70), (1840, 72)], fill=subtle_line)
        draw.rectangle([(80, 70), (280, 72)], fill=accent_color)

        # Marca institucional superior
        try:
            # Fuentes de sistema estándar en macOS
            font_brand = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26)
            font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 58)
            font_quote = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 40)
            font_footer = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 28)
        except Exception:
            font_brand = ImageFont.load_default()
            font_title = font_brand
            font_quote = font_brand
            font_footer = font_brand

        draw.text((80, 85), "ADES.CLOUD | INVESTIGACIÓN Y ANÁLISIS ESTRUCTURAL", fill=(190, 195, 205, 255), font=font_brand)

        # Título de escena
        title_text = scene.get("title", "")
        # Ajuste de saltos de línea para el título
        title_lines = self._wrap_text(title_text, max_chars=40)
        curr_y = 280
        for line in title_lines:
            draw.text((120, curr_y), line, fill=(245, 247, 250, 255), font=font_title)
            curr_y += 75

        # Cita destacada o concepto en pantalla
        quote = scene.get("overlay_quote", "")
        if quote and quote != title_text:
            draw.rectangle([(120, curr_y + 30), (124, curr_y + 160)], fill=accent_color)
            quote_lines = self._wrap_text(f"«{quote}»", max_chars=55)
            q_y = curr_y + 35
            for ql in quote_lines[:3]:
                draw.text((145, q_y), ql, fill=(210, 218, 230, 255), font=font_quote)
                q_y += 50

        # Pie de página con enlace institucional
        draw.rectangle([(80, 990), (1840, 992)], fill=subtle_line)
        draw.text((80, 1005), "https://ades.cloud", fill=(218, 54, 54, 255), font=font_footer)
        draw.text((1500, 1005), "CRÍTICA DE LA ECONOMÍA POLÍTICA", fill=(140, 145, 155, 255), font=font_brand)

        img.save(output_path, "JPEG", quality=95)
        return output_path

    def _wrap_text(self, text: str, max_chars: int = 50) -> List[str]:
        """Envuelve texto en varias líneas sin cortar palabras."""
        words = text.split()
        lines = []
        current = []
        for w in words:
            if sum(len(x) + 1 for x in current) + len(w) <= max_chars:
                current.append(w)
            else:
                if current:
                    lines.append(" ".join(current))
                current = [w]
        if current:
            lines.append(" ".join(current))
        return lines
