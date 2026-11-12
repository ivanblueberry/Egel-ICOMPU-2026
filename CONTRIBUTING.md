# Cómo contribuir

Gracias por ayudar a mantener una guía gratuita, verificable y segura para estudiantes.

## Regla de confidencialidad

No envíes contenido obtenido durante, antes o después de una aplicación real de Ceneval. Esto incluye:

- preguntas, opciones o respuestas recordadas;
- fotografías, capturas, audios o transcripciones;
- descripciones que permitan reconstruir un reactivo;
- bancos recopilados en grupos o servicios de mensajería;
- adaptaciones que solo cambien nombres, cifras u orden de opciones de una pregunta real.

Si no puedes demostrar que un ejercicio fue creado desde conceptos y fuentes públicas, no lo propongas. Para reportar una posible filtración usa [SECURITY.md](SECURITY.md), sin copiar el material en una issue.

## Requisitos de una contribución

1. Escribe contenido original o identifica una licencia compatible.
2. Añade fuentes técnicas verificables; una fuente apoya el concepto, no convierte en reutilizable su redacción.
3. Redacta distractores plausibles y explica por qué cada alternativa es correcta o incorrecta.
4. Evita afirmar que un tema, formato o pregunta aparecerá en el examen real.
5. Declara el uso material de IA y revisa manualmente exactitud, originalidad y referencias.
6. Acepta que el contenido educativo se publicará bajo CC BY-SA 4.0 y el código bajo MIT.

Al enviar un pull request confirmas que tienes derecho a licenciar tu aportación bajo esas condiciones.

## Flujo de trabajo

```sh
python3 -m pip install -r requirements-dev.txt
export SOURCE_DATE_EPOCH=1794441600  # 2026-11-12 00:00:00 UTC
python3 tools/generar.py
python3 tools/verificar.py
python3 -m unittest discover -s tests
python3 tools/auditar_publicacion.py --all-files
tectonic -X compile guia/main.tex --reruns 1 --keep-intermediates --keep-logs
tectonic -X compile guia/main.tex --reruns 1 --keep-intermediates --keep-logs
cp guia/main.pdf dist/Guia-EGEL-Plus-ICOMPU.pdf
python3 tools/verificar_pdf.py
git diff --exit-code
```

Los cambios en los TSV deben regenerar `guia/datos/reactivos.json`, `guia/capitulos/reactivos.tex`, `guia/capitulos/soluciones.tex` y `guia/capitulos/claves.tex`. No edites esos derivados como fuente primaria.

## Estilo editorial

- Español claro, preciso e inclusivo sin sacrificar exactitud técnica.
- Sistema Internacional de unidades y supuestos explícitos.
- Una sola respuesta inequívocamente mejor por reactivo.
- Sin promesas de aprobación ni equivalencias con puntajes oficiales.
- Referencias permanentes o institucionales cuando estén disponibles.
