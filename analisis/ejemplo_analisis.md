# Análisis de la Dinámica del Capital y la Acumulación Contemporánea

> **Documento de Diagnóstico Socioeconómico y Político**
> **Autor:** Investigador Marxista | Proyecto BrainPolitics

---

## 1. Planteamiento del Problema

El análisis de la acumulación de capital en el siglo XXI requiere problematizar la supuesta "desmaterialización" de la economía. Lejos de haber superado las leyes del valor formuladas en la crítica marxista, presenciamos una intensificación de la **composición orgánica del capital** y una exacerbación de las contradicciones de clase.

> [!NOTE]
> La ley de la tendencia decreciente de la tasa de ganancia continúa operando como la contradicción interna fundamental del modo de producción capitalista.

### 1.1. Determinaciones de la Fuerza de Trabajo

La fuerza de trabajo no puede ser reducida al concepto burgués de *"capital humano"*. La relación asalariada implica la subsunción formal y real del trabajo en el capital, donde el **plusvalor** es extraído mediante el incremento de la productividad y la intensificación de la jornada laboral.

---

## 2. Comparación de Categorías teóricas

| Categoría Neoliberal / Burguesa | Categoría Marxista Rigurosa | Determinación Estructural |
| :--- | :--- | :--- |
| Capital Humano | Fuerza de Trabajo | Capacidad física y mental del proletario vendida como mercancía. |
| Colaboradores | Proletariado / Clase Asalariada | Sujetos desposeídos de los medios de producción. |
| Desigualdad de Ingresos | Relaciones de Explotación | Apropiación privada de la plusvalía socialmente producida. |
| Ineficiencia del Estado | Ilusión del Estado Burgués | El Estado como garante de la reproducción de las relaciones de capital. |

---

## 3. Demostración Matemática del Incremento de la Plusvalía

Consideremos la tasa de plusvalía ($p'$) definida en términos de plusvalor ($p$) sobre capital variable ($v$):

$$ p' = \frac{p}{v} $$

En términos computacionales y de modelado cinético en Python:

```python
import numpy as np

def calcular_tasa_plusvalia(plusvalor: float, capital_variable: float) -> float:
    """Calcula la tasa de plusvalía (explotación) p' = p / v."""
    if capital_variable <= 0:
        raise ValueError("El capital variable debe ser mayor que cero.")
    return np.round(plusvalor / capital_variable, 4)

# Ejemplo: Plusvalor = $500, Capital Variable = $200
p_prime = calcular_tasa_plusvalia(500.0, 200.0)
print(f"Tasa de plusvalía (p'): {p_prime * 100}%")
```

---

## 4. Conclusiones e Implicaciones Políticas

1. **Rigor Categorial:** Mantener la claridad terminológica para desarticular la ideología dominante.
2. **Organización del Análisis:** Todos los informes deben archivarse de manera sistemática en carpetas según su formato (`analisis/`, `articulo/`, `folleto/`, etc.).
3. **Perspectiva Histórica:** Ningún fenómeno social puede comprenderse al margen de la lucha de clases y la totalidad social.
