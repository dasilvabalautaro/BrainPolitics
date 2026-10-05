"""
Módulo 'Nerve' (Motor de Inferencia y Renderizado PDF).
Arquitectura Dual-Runtime: Ejecuta la transformación del documento Markdown a HTML
y su compilación final en un PDF de alta calidad estética usando WeasyPrint.
"""

import re
import os
import datetime
from typing import Optional
import markdown
import weasyprint
from .pdf_brain import LayoutBrain


class PDFNerve:
    """Motor de conversión e inferencia visual de Markdown a PDF."""

    def __init__(self):
        self.brain = LayoutBrain()

    def preprocess_callouts(self, md_content: str) -> str:
        """Transforma alertas estilo GitHub/Obsidian (> [!NOTE], etc.) en cajas visuales HTML."""
        callout_types = {
            "NOTE": ("Nota Informativa", "#2563eb", "#eff6ff"),
            "TIP": ("Sugerencia Teórica", "#059669", "#ecfdf5"),
            "IMPORTANT": ("Punto Crucial", "#7c3aed", "#f5f3ff"),
            "WARNING": ("Advertencia Crítica", "#d97706", "#fffbeb"),
            "CAUTION": ("Atención Requerida", "#dc2626", "#fef2f2")
        }

        def _replace_callout(match):
            ctype = match.group(1).upper()
            body = match.group(2).strip()
            title_text, border_color, bg_color = callout_types.get(
                ctype, ("Nota", "#4b5563", "#f9fafb")
            )
            body_clean = re.sub(r'^\s*>\s?', '', body, flags=re.MULTILINE)
            return (
                f'<div class="callout-box" style="border-left: 4px solid {border_color}; background-color: {bg_color};">'
                f'<div class="callout-title" style="color: {border_color};">{title_text}</div>'
                f'<div class="callout-body">{body_clean}</div>'
                f'</div>'
            )

        pattern = r'>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:>\s?.*\n?)+)'
        return re.sub(pattern, _replace_callout, md_content, flags=re.IGNORECASE)

    def generate_css(self, metrics: dict, title: str) -> str:
        """Genera el diseño CSS profesional con estándar W3C CSS Paged Media."""
        colors = metrics["colors"]
        base_font = metrics["base_font_pt"]
        line_height = metrics["line_height"]

        css = f"""
        @page {{
            size: A4 portrait;
            margin: 2.5cm 2.0cm 2.0cm 2.0cm;
            @top-left {{
                content: "ADES.CLOUD | {title}";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
                border-bottom: 1px solid {colors['border']};
                padding-bottom: 4px;
            }}
            @top-right {{
                content: "Investigación Marxista";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
                border-bottom: 1px solid {colors['border']};
                padding-bottom: 4px;
            }}
            @bottom-left {{
                content: "Documento de Uso Político e Investigativo";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
                border-top: 1px solid {colors['border']};
                padding-top: 4px;
            }}
            @bottom-right {{
                content: "Página " counter(page) " de " counter(pages);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
                border-top: 1px solid {colors['border']};
                padding-top: 4px;
            }}
        }}

        @page:first {{
            margin: 2.0cm 2.0cm 2.0cm 2.0cm;
            @top-left {{ content: normal; border: none; }}
            @top-right {{ content: normal; border: none; }}
            @bottom-left {{ content: normal; border: none; }}
            @bottom-right {{ content: normal; border: none; }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: {base_font}pt;
            line-height: {line_height};
            color: {colors['text']};
            text-align: justify;
        }}

        /* Portada para Presentación Pública (Diagramación basada en Bloques) */
        .cover-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 2.5cm;
            padding-bottom: 1.0cm;
            width: 100%;
            display: block;
            box-sizing: border-box;
        }}

        .cover-badge-wrapper {{
            text-align: center;
            margin-bottom: 25px;
            width: 100%;
        }}

        .cover-badge {{
            display: inline-block;
            font-size: 8.5pt;
            font-weight: 700;
            color: {colors['accent']};
            text-transform: uppercase;
            letter-spacing: 2px;
            background-color: #fce8e8;
            padding: 6px 16px;
            border-radius: 16px;
        }}

        .cover-title {{
            font-size: 24pt;
            font-weight: 800;
            color: {colors['primary']};
            line-height: 1.3;
            margin-top: 15px;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
            text-align: center;
            width: 100%;
            display: block;
        }}

        .cover-divider {{
            width: 80px;
            height: 3px;
            background-color: {colors['accent']};
            margin: 25px auto 30px auto;
            display: block;
            border: none;
        }}

        .cover-subtitle {{
            font-size: 11pt;
            color: #475569;
            margin-bottom: 40px;
            font-style: italic;
            text-align: center;
            width: 100%;
            display: block;
        }}

        .cover-meta {{
            font-size: 9.5pt;
            color: #64748b;
            margin-top: 4.5cm;
            line-height: 1.8;
            border-top: 1px solid {colors['border']};
            padding-top: 25px;
            text-align: center;
            width: 100%;
            display: block;
        }}

        .main-content {{
            width: 100%;
            display: block;
        }}

        /* Encabezados */
        h1 {{
            font-size: 17pt;
            font-weight: 700;
            color: {colors['primary']};
            border-bottom: 2px solid {colors['accent']};
            padding-bottom: 4px;
            margin-top: 22px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}
        h2 {{
            font-size: 13pt;
            font-weight: 700;
            color: {colors['primary']};
            margin-top: 18px;
            margin-bottom: 8px;
            border-bottom: 1px solid {colors['border']};
            padding-bottom: 3px;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 11pt;
            font-weight: 700;
            color: {colors['accent']};
            margin-top: 14px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
        }}

        /* Citas y Bloques Críticos */
        blockquote {{
            background-color: {colors['bg_subtle']};
            border-left: 4px solid {colors['accent']};
            margin: 14px 0;
            padding: 10px 14px;
            font-style: italic;
            color: #334155;
            border-radius: 0 4px 4px 0;
        }}

        /* Alertas / Callouts */
        .callout-box {{
            margin: 14px 0;
            padding: 10px 14px;
            border-radius: 4px;
        }}
        .callout-title {{
            font-weight: 700;
            font-size: 8.5pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}
        .callout-body {{
            font-size: 9pt;
            color: #1e293b;
        }}

        /* Tablas */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}
        th {{
            background-color: {colors['primary']};
            color: #ffffff;
            font-weight: 700;
            padding: 8px 10px;
            text-align: left;
            border: 1px solid {colors['primary']};
        }}
        td {{
            padding: 6px 10px;
            border: 1px solid {colors['border']};
        }}
        tr:nth-child(even) {{
            background-color: {colors['bg_subtle']};
        }}

        /* Código */
        pre, code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 8.5pt;
        }}
        code {{
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        pre {{
            background-color: #1e293b;
            color: #f8fafc;
            padding: 12px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 14px 0;
            page-break-inside: avoid;
        }}
        pre code {{
            background-color: transparent;
            color: #f8fafc;
            padding: 0;
        }}

        ul, ol {{
            margin-top: 0;
            margin-bottom: 10px;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 4px;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: {colors['border']};
            margin: 20px 0;
        }}
        """
        return css

    def build_full_html(self, md_content: str, title: str, include_cover: bool = True, preset: str = "marxist_editorial") -> str:
        """Compila el HTML estructurado listo para WeasyPrint."""
        processed_md = self.preprocess_callouts(md_content)

        if not title:
            h1_match = re.search(r'^\s*#\s+(.+)$', md_content, re.MULTILINE)
            title = h1_match.group(1).strip() if h1_match else "Documento de Investigación"

        metrics = self.brain.compute_layout_metrics(md_content, preset=preset)
        css_style = self.generate_css(metrics, title)

        md_engine = markdown.Markdown(extensions=[
            'tables', 'fenced_code', 'codehilite', 'toc', 'nl2br', 'sane_lists', 'footnotes', 'attr_list'
        ])
        body_html = md_engine.convert(processed_md)
        date_str = datetime.datetime.now().strftime("%d de %B de %Y")

        html_doc = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
            {css_style}
            </style>
        </head>
        <body>
        """

        if include_cover:
            html_doc += f"""
            <div class="cover-page">
                <div class="cover-badge-wrapper">
                    <span class="cover-badge">ADES.CLOUD — Centro de Estudios e Investigación Marxista</span>
                </div>
                <div class="cover-title">{title}</div>
                <div class="cover-divider"></div>
                <div class="cover-subtitle">Ciencias Sociales, Investigación Histórica y Economía Política Marxista</div>
                <div class="cover-meta">
                    <strong>Elaborado por:</strong> Centro de investigación marxista ADES.CLOUD.<br>
                    <strong>Fecha de Emisión:</strong> {date_str}<br>
                    <strong>Formato:</strong> Documento Teórico / Presentación Pública
                </div>
            </div>
            """

        html_doc += f"""
            <div class="main-content">
                {body_html}
            </div>
        </body>
        </html>
        """
        return html_doc

    def render_pdf(self, md_content: str, output_path: str, title: Optional[str] = None, include_cover: bool = True, preset: str = "marxist_editorial") -> bool:
        """Genera el archivo PDF profesional desde el contenido Markdown."""
        html_content = self.build_full_html(md_content, title=title, include_cover=include_cover, preset=preset)

        out_dir = os.path.dirname(os.path.abspath(output_path))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        weasyprint.HTML(string=html_content).write_pdf(output_path)
        return os.path.exists(output_path)
