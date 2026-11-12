# Guía abierta EGEL Plus ICOMPU

Material independiente y gratuito para preparar el **EGEL Plus en Ingeniería Computacional**. Incluye teoría, ejemplos desarrollados, 360 reactivos originales con soluciones razonadas y una ruta de estudio de 12 semanas.

> [!IMPORTANT]
> Este proyecto no es una publicación de Ceneval, no está avalado por esa institución y no contiene preguntas obtenidas de una aplicación real. Los resultados del banco no equivalen al índice Ceneval ni garantizan aprobar el examen.

## Descargar y comenzar

- **[Descargar la guía completa en PDF](dist/Guia-EGEL-Plus-ICOMPU.pdf)**
- **[Seguir el plan de estudio de 12 semanas](docs/plan-12-semanas.md)**
- Consultar la [guía pública del sustentante de Ceneval, edición enero de 2023](https://ceneval.edu.mx/wp-content/uploads/2023/01/GUIA-EGEL-ICOMPU.pdf), verificada por última vez el 12 de noviembre de 2026.

Antes de estudiar, responde una muestra sin apuntes y abre una bitácora. Para cada error registra el identificador, la causa, la corrección y la fecha en que volverás a resolverlo. No cuentes como dominio un acierto por adivinación.

## Contenido

La guía desarrolla las tres áreas disciplinares y la sección transversal:

| Área | Contenido de práctica |
| --- | ---: |
| Implementación de hardware | 100 reactivos |
| Implementación de redes de computadoras | 100 reactivos |
| Implementación de software | 100 reactivos |
| Comprensión lectora | 30 reactivos |
| Redacción indirecta | 30 reactivos |

Los 360 reactivos y sus textos de lectura son material original de práctica. No están calibrados psicométricamente, no predicen preguntas específicas y no reproducen la ponderación oficial.

## Ruta de 12 semanas

La ruta base propone cinco sesiones y entre seis y ocho horas por semana:

1. Diagnóstico, método y bitácora.
2. Circuitos, electrónica y lógica digital.
3. Arquitectura y sistemas embebidos.
4. Señales, sensores, automatización y control.
5. Diseño y direccionamiento de redes.
6. Administración y seguridad de redes.
7. Ingeniería de software e interacción humano-computadora.
8. Programación, compiladores y sistemas operativos.
9. Datos, algoritmos, bases de datos e inteligencia artificial.
10. Integración y recuperación de temas débiles.
11. Simulacro mixto y remediación.
12. Simulacro final, repaso espaciado y logística.

Comprensión lectora y redacción se practican todas las semanas. El [calendario detallado](docs/plan-12-semanas.md) contiene objetivos, capítulos, rangos de preguntas, productos semanales y criterios de avance, además de variantes de cuatro y diez horas.

## Compilar y verificar

Requisitos: Python 3.11 o posterior, [Tectonic](https://tectonic-typesetting.github.io/) y las dependencias de `requirements-dev.txt` para la inspección avanzada del PDF.

```sh
python3 -m pip install -r requirements-dev.txt
export SOURCE_DATE_EPOCH=1794441600  # 2026-11-12 00:00:00 UTC
python3 tools/generar.py
python3 tools/verificar.py
python3 tools/auditar_publicacion.py --all-files
tectonic -X compile guia/main.tex --reruns 1 --keep-intermediates --keep-logs
tectonic -X compile guia/main.tex --reruns 1 --keep-intermediates --keep-logs
cp guia/main.pdf dist/Guia-EGEL-Plus-ICOMPU.pdf
python3 tools/verificar_pdf.py
```

Después de regenerar, `git diff --exit-code` debe quedar limpio. La integración continua ejecuta estas comprobaciones en cada cambio y publica el PDF al crear una etiqueta `v*`.

## Contribuir responsablemente

Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir un cambio. No aceptamos preguntas, respuestas, fotografías, transcripciones ni descripciones reconstruidas a partir de una aplicación real, aunque se compartan gratuitamente. Las contribuciones deben ser originales o contar con una licencia compatible y citar fuentes verificables.

Si detectas posible contenido confidencial, no lo pegues en una incidencia pública: sigue el canal privado descrito en [SECURITY.md](SECURITY.md).

## Autoría, IA y licencias

Proyecto de [@ivanblueberry](https://github.com/ivanblueberry), elaborado con asistencia de inteligencia artificial y revisión humana. La IA se utilizó como apoyo de redacción, organización y comprobación; la responsabilidad editorial corresponde al mantenedor.

- Guía, reactivos, soluciones, diagramas y datos educativos: [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt).
- Código en `tools/` y `tests/`: [MIT](LICENSES/MIT.txt).
- Las obras, marcas y fuentes citadas conservan los derechos y condiciones de sus titulares.

Consulta [LICENSES/README.md](LICENSES/README.md) para conocer el alcance exacto y [DISCLAIMER.md](DISCLAIMER.md) para los límites del proyecto.

### Cita sugerida

> @ivanblueberry (2026). *Guía abierta EGEL Plus ICOMPU* (versión 1.0.0). GitHub. https://github.com/ivanblueberry/Egel-ICOMPU-2026
