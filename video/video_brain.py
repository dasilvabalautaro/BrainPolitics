"""
Módulo 'Brain' (Inteligencia Temporal, Guionización y Modelado Dialéctico).
Arquitectura Dual-Runtime: Procesa el documento Markdown y calcula matrices de
duración, velocidad de habla (WPM), pausas cognitivas y descriptores fotográficos
utilizando NumPy.
"""

import re
from typing import List, Dict, Any, Tuple
import numpy as np


class VideoBrain:
    """Inteligencia analítica para estructurar guiones audiovisuales a partir de Markdown."""

    def __init__(self, target_wpm: float = 105.0):
        """
        Args:
            target_wpm: Palabras por minuto objetivo para la locución reflexiva de hombre mayor (100-110 WPM).
        """
        self.target_wpm = float(target_wpm)
        # Palabras por segundo
        self.wps = self.target_wpm / 60.0

        # Paletas de color cinemáticas para superposiciones (RGB)
        self.palette = {
            "bg_dark": np.array([18, 22, 28]),          # #12161c
            "accent_crimson": np.array([178, 34, 34]),   # #b22222
            "text_light": np.array([245, 247, 250]),     # #f5f7fa
            "text_subtle": np.array([180, 185, 195]),    # #b4b9c3
            "overlay_scrim": np.array([10, 12, 16]),     # Scrim traslúcido
        }

    def clean_markdown_text(self, text: str) -> str:
        """Normalizador ortofónico estricto: transforma sintaxis Markdown en prosa hablada natural.
        
        Elimina completamente código, fórmulas, símbolos ortográficos, viñetas y caracteres
        que los sintetizadores de voz leen como palabras ('guión', 'barra', 'asterisco', etc.).
        """
        import re

        # 1. Eliminar bloques de código completos (incluyendo código multilínea)
        text = re.sub(r"```[\s\S]*?```", "", text)
        # 2. Eliminar código inline (ej. `analisis/`, `variable`)
        text = re.sub(r"`[^`\n]*`", "", text)
        # 3. Eliminar tablas completas en Markdown
        text = re.sub(r"\|[^\n]+\|", "", text)
        # 4. Eliminar fórmulas matemáticas LaTeX
        text = re.sub(r"\$\$[\s\S]*?\$\$", "", text)
        text = re.sub(r"\$[^\$\n]+\$", "", text)
        # 5. Eliminar metadatos de autoría y callouts
        text = re.sub(r"^>\s*\[![A-Z]+\].*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>\s*\*?\*?Autor:?\*?\*?.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>\s*\*?\*?Documento:?\*?\*?.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
        # 6. Eliminar separadores horizontales (evitar que lea 'guión guión guión')
        text = re.sub(r"^[-\*_]{3,}\s*$", "", text, flags=re.MULTILINE)
        # 7. Eliminar viñetas y numeraciones al inicio de línea para evitar la palabra 'guión' o 'uno punto'
        text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*\d+[\.\)]\s+", "", text, flags=re.MULTILINE)
        # 8. Traducir siglos romanos a texto fonético en español
        text = re.sub(r"\bsiglo\s+XXI\b", "siglo veintiuno", text, flags=re.IGNORECASE)
        text = re.sub(r"\bsiglo\s+XX\b", "siglo veinte", text, flags=re.IGNORECASE)
        text = re.sub(r"\bsiglo\s+XIX\b", "siglo diecinueve", text, flags=re.IGNORECASE)
        text = re.sub(r"\bsiglo\s+XVIII\b", "siglo dieciocho", text, flags=re.IGNORECASE)
        # 9. Eliminar enlaces markdown dejando solo el texto legible
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        # 10. Erradicar cualquier guión restante (para que NUNCA pronuncie 'guión')
        text = re.sub(r"\s+-\s+", ", ", text)
        text = re.sub(r"[-–—]", " ", text)
        # 11. Eliminar símbolos ortográficos que el TTS lee literalmente (barras, plecas, corchetes)
        text = re.sub(r"[/|\\#~^<>{}\[\]\(\)]", " ", text)
        # 12. Eliminar marcas de negrita o cursiva residuales
        text = re.sub(r"(\*\*|\*|__)", "", text)
        # 13. Limpiar paréntesis y signos duplicados
        text = re.sub(r"\s+([,\.\:\;])", r"\1", text)
        text = re.sub(r"[,]{2,}", ",", text)
        text = re.sub(r"[\.]{2,}", ".", text)
        # 14. Normalizar espacios en blanco
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_document_title(self, md_content: str) -> str:
        """Extrae el título principal del documento limpiando numeraciones residuales."""
        import re
        match = re.search(r"^#\s+(.+)$", md_content, flags=re.MULTILINE)
        if match:
            clean = re.sub(r"^[\d\.\-\s]+", "", match.group(1)).strip()
            return clean
        return "Análisis Político y Económico | ADES.CLOUD"

    def parse_scenes(self, md_content: str) -> List[Dict[str, Any]]:
        """Parsea el contenido Markdown y lo descompone en escenas cinematográficas lógicas.

        Cada escena cuenta con:
        - title: Título temático limpio (sin puntos ni números residuales)
        - narration: Prosa hablada fluida y normalizada (sin sintaxis técnica)
        - overlay_quote: Texto destacado para tercios de pantalla
        - search_terms: Términos para búsqueda de fotografía documental
        - duration: Duración en segundos calculada con NumPy
        - effect: Efecto de cámara Ken Burns
        """
        import re
        scenes = []
        raw_sections = re.split(r"\n(?=##\s+)", md_content)

        main_title = self.extract_document_title(md_content)

        # Escena 0: Introducción / Título Principal
        # Buscar el primer párrafo temático sustantivo evitando metadatos
        intro_text = ""
        intro_raw = raw_sections[0] if raw_sections else ""
        intro_lines = intro_raw.split("\n")
        intro_clean_paras = []
        for line in intro_lines:
            if line.startswith("#") or line.startswith(">") or line.startswith("-") or not line.strip():
                continue
            cleaned = self.clean_markdown_text(line)
            if len(cleaned) > 25:
                intro_clean_paras.append(cleaned)

        if intro_clean_paras:
            intro_text = " ".join(intro_clean_paras)[:280]
        else:
            intro_text = "Presentamos una investigación teórica y estructural elaborada por el Centro de Estudios e Investigación Marxista ADES.CLOUD."

        scenes.append({
            "scene_index": 0,
            "section_type": "intro",
            "title": main_title,
            "narration": f"{main_title}. {intro_text}",
            "overlay_quote": main_title,
            "search_terms": [
                "Plaza Murillo La Paz Bolivia",
                "Palacio Quemado La Paz Bolivia",
                "Cerro Rico Potosi miners",
                "United States Department of State",
            ],
            "effect": "zoom_in",
        })

        effects_cycle = ["pan_left", "zoom_out", "pan_right", "zoom_in"]
        eff_idx = 0

        # Procesar secciones de nivel 2 (##)
        for section in raw_sections:
            if not section.strip().startswith("##"):
                continue

            sec_lines = section.strip().split("\n")
            sec_header = sec_lines[0].replace("##", "").strip()
            # Limpiar numeración absoluta: romanos ('I. ', 'IV. '), arábigos ('1. ', '1.1. ') y guiones
            sec_clean_title = re.sub(r"^([IVXLCDM]+\.?|\d+(\.\d+)*\.?|\-)\s*", "", sec_header, flags=re.IGNORECASE).strip()

            body_content = "\n".join(sec_lines[1:])
            # Eliminar bloques de código antes del split para evitar contaminar párrafos
            body_no_code = re.sub(r"```[\s\S]*?```", "", body_content)
            body_no_math = re.sub(r"\$\$[\s\S]*?\$\$", "", body_no_code)

            paragraphs = [p.strip() for p in body_no_math.split("\n\n") if p.strip()]

            filtered_paras = []
            quote_text = ""
            for p in paragraphs:
                if p.startswith("|") or p.startswith("```") or p.startswith("$$"):
                    continue
                clean_p = self.clean_markdown_text(p)
                if len(clean_p) > 25:
                    filtered_paras.append(clean_p)
                if p.startswith(">") and not quote_text:
                    quote_text = self.clean_markdown_text(p)

            if not filtered_paras:
                continue

            full_narration = " ".join(filtered_paras)
            if len(full_narration) > 450:
                # Cortar en la última oración completa antes de 450 caracteres
                last_dot = full_narration[:450].rfind(".")
                if last_dot > 150:
                    narration_chunk = full_narration[:last_dot + 1]
                else:
                    last_space = full_narration[:450].rfind(" ")
                    narration_chunk = full_narration[:last_space] + "."
            else:
                narration_chunk = full_narration

            thematic_quote = self._extract_thematic_quote(sec_clean_title, body_content)
            search_query = self._generate_photo_keywords(sec_clean_title, narration_chunk)

            scenes.append({
                "scene_index": len(scenes),
                "section_type": "content",
                "title": sec_clean_title,
                "narration": narration_chunk,
                "overlay_quote": thematic_quote,
                "search_terms": search_query,
                "effect": effects_cycle[eff_idx % len(effects_cycle)],
            })
            eff_idx += 1

        # Escena Final Obligatoria: Cierre Institucional ADES.CLOUD
        scenes.append({
            "scene_index": len(scenes),
            "section_type": "outro",
            "title": "ADES.CLOUD | Centro de Estudios e Investigación Marxista",
            "narration": (
                "Para profundizar en este análisis y acceder a todos nuestros escritos, "
                "investigaciones y documentos teóricos, te invitamos a visitar ades.cloud."
            ),
            "overlay_quote": "Consulta todos nuestros escritos en https://ades.cloud",
            "search_terms": [
                "Cerro Rico Potosi miners",
                "Demonstration La Paz Bolivia",
                "Plaza Murillo La Paz Bolivia"
            ],
            "effect": "zoom_in",
        })

        # Cálculo dinámico de duraciones mediante NumPy
        scenes = self.compute_scene_timings(scenes)
        return scenes

    def _extract_thematic_quote(self, title: str, text: str) -> str:
        """Extrae o sintetiza una tesis o cita conceptual completa y autocontenida para el zócalo de la escena."""
        clean_text = self.clean_markdown_text(text)
        t_low = f"{title} {clean_text}".lower()

        # Detección contextual por título de sección de tesis categoriales de ADES.CLOUD
        t_clean = title.lower()
        if any(w in t_clean for w in ["purga", "judicial"]):
            return "La purga judicial evidencia el vasallaje colonial hacia la administración de Washington."
        elif any(w in t_clean for w in ["fundamentos", "compradora", "imperialismo"]):
            return "El imperialismo es la fase monopolista caracterizada por el dominio del capital financiero."
        elif any(w in t_clean for w in ["bancarrota", "salvaciones", "reformistas"]):
            return "Esperar que las instituciones del parlamentarismo burgués frenen al imperialismo es un desatino."
        elif any(w in t_clean for w in ["autoemancipación", "programa"]):
            return "La emancipación de la clase obrera debe ser obra de los trabajadores mismos."
        elif any(w in t_clean for w in ["conclusión", "verdad"]):
            return "La verdad es siempre revolucionaria: frente al imperialismo, autoemancipación proletaria."

        # Descomponer en oraciones limpias completas
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_text) if len(s.strip()) >= 35]
        for s in sentences:
            if 50 <= len(s) <= 120:
                return s

        if sentences:
            s0 = sentences[0]
            if len(s0) <= 120:
                return s0
            clipped = s0[:115]
            last_space = clipped.rfind(" ")
            if last_space > 35:
                return clipped[:last_space].rstrip(".,;:-") + "..."

        return title

    def _generate_photo_keywords(self, title: str, text: str) -> List[str]:
        """Genera descriptores de búsqueda estrictamente fotográficos contextuales al documento."""
        t_clean = title.lower()

        # Detección contextual por sección temática
        if any(w in t_clean for w in ["purga", "judicial"]):
            return [
                "Marco Rubio",
                "Viru Viru Santa Cruz Bolivia",
                "Palacio Quemado La Paz Bolivia",
                "Plaza Murillo La Paz Bolivia",
                "United States Department of State"
            ]
        elif any(w in t_clean for w in ["fundamentos", "compradora", "imperialismo"]):
            return [
                "Cooperative Miner Cerro Rico Potosi photo",
                "Salar de Uyuni lithium Bolivia",
                "Wall Street stock exchange New York",
                "New York Stock Exchange"
            ]
        elif any(w in t_clean for w in ["bancarrota", "salvaciones", "reformistas"]):
            return [
                "Pan American Building OAS Washington",
                "United States Capitol building Washington",
                "Demonstration La Paz Bolivia",
                "Plaza Murillo La Paz Bolivia"
            ]
        elif any(w in t_clean for w in ["autoemancipación", "programa"]):
            return [
                "Karl Marx portrait photograph",
                "Vladimir Lenin portrait photograph",
                "Demonstration La Paz Bolivia",
                "Cooperative Miner Cerro Rico Potosi photo"
            ]
        elif any(w in t_clean for w in ["conclusión", "verdad"]):
            return [
                "Plaza Murillo La Paz Bolivia",
                "Demonstration La Paz Bolivia",
                "Palacio Quemado La Paz Bolivia"
            ]

        # Descriptores de respaldo
        base_words = re.findall(r"\b[A-Za-zÁ-ú]{4,}\b", f"{title} {text}")
        stopwords = {
            "para", "como", "este", "esta", "estos", "estas", "sobre", "entre", "hacia",
            "desde", "según", "donde", "cuando", "quien", "cual", "forma", "punto", "hacer"
        }
        filtered = [w.lower() for w in base_words if w.lower() not in stopwords]
        primary_term = " ".join(filtered[:3]) if filtered else "social economy history"

        return [
            f"{primary_term} documentary photography",
            f"{primary_term} historical archive photo",
            "industrial workers social movement historical photograph",
        ]

    def compute_scene_timings(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aplica cálculo matricial con NumPy para estimar duraciones de exposición óptimas."""
        word_counts = np.array([len(s["narration"].split()) for s in scenes], dtype=np.float64)

        # Duración base de lectura según WPS (palabras por segundo)
        raw_durations = word_counts / max(0.1, self.wps)

        # Factor de peso cognitivo por tipo de sección (pausas reflexivas de hombre mayor)
        type_weights = []
        for s in scenes:
            if s["section_type"] == "intro":
                type_weights.append(1.35)  # Margen amplio para fijar el tema inicial
            elif s["section_type"] == "outro":
                type_weights.append(1.45)  # Tiempo pausado para el cierre de ades.cloud
            else:
                type_weights.append(1.30)  # Margen de asimilación conceptual para argumentos teóricos

        weights_arr = np.array(type_weights, dtype=np.float64)

        # Duraciones ponderadas con NumPy
        weighted_durations = raw_durations * weights_arr

        # Limitar dentro de rangos cinematográficos pausados:
        # Mínimo 10.0 segundos por escena, máximo 40.0 segundos para mantener solidez expositiva
        clamped_durations = np.clip(weighted_durations, 10.0, 40.0)

        # Redondear a décimas de segundo
        final_durations = np.round(clamped_durations, 1)

        for i, s in enumerate(scenes):
            s["duration"] = float(final_durations[i])
            s["word_count"] = int(word_counts[i])

        return scenes

    def generate_youtube_metadata(self, doc_title: str, scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Genera automáticamente los metadatos optimizados para YouTube (título, descripción, marcas de tiempo)."""
        cumulative_time = 0.0
        timestamps = []

        for s in scenes:
            mins = int(cumulative_time // 60)
            secs = int(cumulative_time % 60)
            time_str = f"{mins:02d}:{secs:02d}"
            
            label = s["title"]
            if s["section_type"] == "outro":
                label = "Conclusión y Recursos en ades.cloud"
            
            timestamps.append(f"{time_str} - {label}")
            cumulative_time += s["duration"]

        timestamps_block = "\n".join(timestamps)

        description = (
            f"Análisis estructural e investigación teórica por ADES.CLOUD.\n\n"
            f"🔗 Lee el documento completo y accede a todos nuestros análisis en:\n"
            f"👉 https://ades.cloud\n\n"
            f"Capítulos y Marcas de Tiempo:\n"
            f"{timestamps_block}\n\n"
            f"---\n"
            f"Producido por el Centro de Estudios e Investigación Marxista ADES.CLOUD.\n"
            f"Rigor categorial, materialismo histórico y crítica de la economía política."
        )

        return {
            "title": f"{doc_title} | Análisis Crítico ADES.CLOUD",
            "description": description,
            "total_duration_sec": float(cumulative_time),
            "timestamps": timestamps,
        }
