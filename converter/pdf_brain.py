"""
Módulo 'Brain' (Inteligencia de Maquetación y Diseño).
Arquitectura Dual-Runtime: Procesa métricas de texto y calcula parámetros óptimos
de tipografía, contraste y diagramación visual usando NumPy.
"""

import numpy as np


class LayoutBrain:
    """Inteligencia analítica para calcular proporciones de diagramación en PDF."""

    def __init__(self):
        # Paletas de color optimizadas para presentaciones públicas (RGB en rango 0.0 - 1.0)
        self.palettes = {
            "marxist_editorial": {
                "primary": np.array([0.118, 0.133, 0.165]),      # Obsidian Dark (#1e222a)
                "accent": np.array([0.620, 0.106, 0.106]),       # Crimson Accent (#9e1b1b)
                "text": np.array([0.168, 0.176, 0.259]),         # Deep Charcoal (#2b2d42)
                "bg_subtle": np.array([0.972, 0.976, 0.980]),    # Off-white (#f8f9fa)
                "border": np.array([0.886, 0.910, 0.941]),       # Subdued border (#e2e8f0)
            },
            "academic_dark": {
                "primary": np.array([0.05, 0.05, 0.08]),
                "accent": np.array([0.75, 0.20, 0.20]),
                "text": np.array([0.20, 0.20, 0.25]),
                "bg_subtle": np.array([0.95, 0.96, 0.97]),
                "border": np.array([0.80, 0.82, 0.85]),
            }
        }

    def compute_layout_metrics(self, raw_text: str, preset: str = "marxist_editorial") -> dict:
        """Calcula los hiperparámetros de renderizado óptimos según la densidad del texto.
        
        Args:
            raw_text: Contenido del archivo Markdown en texto plano.
            preset: Estilo de paleta visual predefinido.
            
        Returns:
            dict con variables de estilos CSS parametrizados dinámicamente.
        """
        char_count = len(raw_text)
        word_count = len(raw_text.split())
        paragraph_count = max(1, raw_text.count("\n\n"))

        # Vector de métricas [palabras_por_parrafo, longitud_promedio_palabra, densidad_texto]
        words_per_para = word_count / float(paragraph_count)
        avg_word_len = char_count / float(max(1, word_count))
        metrics_vec = np.array([words_per_para, avg_word_len, char_count])

        # Estimación matricial de escala tipográfica (base_font_pt, line_height, heading_scale)
        # Para textos más extensos se ajusta levemente el interlineado y margen
        if char_count < 3000:
            font_scale = np.array([10.5, 1.55, 1.80])  # Texto breve (ensayos/resúmenes)
        elif char_count < 15000:
            font_scale = np.array([10.0, 1.50, 1.70])  # Texto mediano (artículos/folletos)
        else:
            font_scale = np.array([9.5, 1.45, 1.60])   # Monografías/investigaciones extensas

        base_font_pt, line_height, heading_scale = font_scale

        # Matriz de colores convertida a sintaxis CSS hex
        palette = self.palettes.get(preset, self.palettes["marxist_editorial"])
        colors_hex = {}
        for key, rgb_vec in palette.items():
            rgb_255 = (rgb_vec * 255).astype(int)
            colors_hex[key] = f"#{rgb_255[0]:02x}{rgb_255[1]:02x}{rgb_255[2]:02x}"

        # Cálculo de presupuesto estimado de páginas
        est_pages = int(np.ceil(word_count / 450.0))

        return {
            "char_count": char_count,
            "word_count": word_count,
            "est_pages": est_pages,
            "base_font_pt": base_font_pt,
            "line_height": line_height,
            "heading_scale": heading_scale,
            "colors": colors_hex,
            "preset": preset
        }
