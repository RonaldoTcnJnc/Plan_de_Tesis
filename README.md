# Plan de tesis y revisión sistemática

Este repositorio contiene dos productos académicos relacionados con el estudio de patrones espaciales y espacio-temporales de incidentes de seguridad ciudadana en San Sebastián, Cusco:

1. **El plan de tesis**, que define la investigación empírica propuesta para los registros del SIPCOP Municipal.
2. **La revisión sistemática de literatura**, que sintetiza estudios previos sobre detección de hotspots y proporciona antecedentes para justificar las decisiones del plan.

Son documentos independientes, con fuentes, bibliografías y formatos LaTeX propios. La revisión informa el marco y la metodología del plan; no forma parte de su compilación.

## Estructura del repositorio

```text
Plan_de_Tesis/
├── README.md
├── Tesis/
│   ├── main.tex
│   ├── chapters/
│   ├── frontmatter/
│   ├── bibliography/
│   ├── datos/
│   ├── figures/
│   └── presentacion/
└── Review/
	├── main.tex
	├── bibliography/
	└── figures/
```

## 1. Plan de tesis

### Propósito

El plan se titula **“Análisis de patrones espacio-temporales de las ocurrencias de seguridad ciudadana mediante técnicas de agrupamiento espacial en el distrito de San Sebastián, Cusco, periodo enero-agosto de 2025”**. Propone analizar la distribución espacial y temporal de ocurrencias de seguridad ciudadana registradas por el SIPCOP Municipal en el distrito de San Sebastián.

El documento desarrolla el planteamiento de la investigación, los antecedentes y el marco teórico, la metodología, la factibilidad, los aspectos administrativos y los anexos. El periodo y las características de los datos que se mencionan en el plan corresponden al extracto descrito en ese documento; deben consultarse allí para conocer su cobertura y limitaciones.

### Contenido

- `Tesis/main.tex`: punto de entrada para compilar el plan.
- `Tesis/frontmatter/`: portada, resumen, agradecimientos, índices e introducción.
- `Tesis/chapters/`: generalidades, marco teórico, metodología, factibilidad, aspectos administrativos y anexos.
- `Tesis/bibliography/references.bib`: referencias del plan.
- `Tesis/bibliography/apalike-es.bst`: estilo bibliográfico usado por el plan.
- `Tesis/datos/sipcop_san_sebastian_2025.csv`: extracto de datos usado por los scripts de diagnóstico.
- `Tesis/datos/diagnostico_preliminar.py`: resumen exploratorio de registros, ubicaciones, duplicados y distribuciones temporales; calcula también distancias a vecinos cercanos. No ejecuta DBSCAN ni pruebas de significancia de hotspots.
- `Tesis/datos/figuras_diagnostico.py`: genera figuras descriptivas en `Tesis/figures/`.
- `Tesis/datos/descargar_sidpol_cusco.py`: descarga registros de SIDPOL para el departamento de Cusco desde un servicio ArcGIS y escribe un CSV junto al script.
- `Tesis/presentacion/presentacion.tex`: fuente de la presentación del proyecto.

### Compilar el plan

Desde la raíz del repositorio:

```sh
cd Tesis
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

El resultado se genera como `Tesis/main.pdf`. Para compilar la presentación:

```sh
cd Tesis/presentacion
latexmk -pdf -interaction=nonstopmode -halt-on-error presentacion.tex
```

La compilación requiere TeX Live y los paquetes usados por el documento, entre ellos `babel-spanish`, `natbib`, `tocloft`, `titlesec`, `algorithm` y TikZ/PGF.

### Ejecutar los scripts de diagnóstico

Los scripts leen el CSV mediante una ruta relativa, por eso deben ejecutarse desde `Tesis/datos/`:

```sh
cd Tesis/datos
python diagnostico_preliminar.py
python figuras_diagnostico.py
```

El primer script imprime estadísticas descriptivas en la terminal. El segundo escribe figuras PDF en `Tesis/figures/`. Se requieren Python 3 y las bibliotecas `pandas`, `numpy`, `scipy`, `scikit-learn` y `matplotlib`.

El descargador de SIDPOL es una fuente de datos distinta del CSV SIPCOP incluido. Si se usa, consulta un servicio web externo y genera `sidpol_cusco.csv` en la carpeta del script:

```sh
cd Tesis/datos
python descargar_sidpol_cusco.py
```

La disponibilidad y el contenido de ese servicio externo pueden cambiar. Revisa las condiciones de uso y la procedencia de los datos antes de redistribuir resultados descargados.

## 2. Revisión sistemática

### Propósito y alcance

La revisión se titula **“Técnicas de agrupamiento espacial y análisis espacio-temporal para la detección de hotspots de incidentes delictivos y de seguridad: una revisión sistemática de la literatura”**. Examina 17 estudios primarios publicados entre 2008 y 2026 y organiza la síntesis alrededor de cuatro preguntas:

- ¿Qué técnicas espaciales y de agrupamiento se utilizan para detectar concentraciones de incidentes?
- ¿Cómo se evalúan la significancia, calidad y robustez de los hotspots?
- ¿Cómo se incorpora la dimensión temporal?
- ¿Qué sesgos y limitaciones de los datos se reportan, y qué evidencia existe para Perú y Latinoamérica?

El manuscrito propone una taxonomía de cinco familias: densidad continua, agrupamiento por densidad, agrupamiento por partición o jerarquía, estadística espacial inferencial y modelos multivariados/econométricos. También expone las limitaciones de cobertura de su búsqueda y selección de estudios.

### Contenido

- `Review/main.tex`: fuente principal del manuscrito.
- `Review/bibliography/references.bib`: referencias bibliográficas.
- `Review/figures/`: carpeta destinada a las figuras del manuscrito.

### Compilar la revisión

Desde la raíz del repositorio:

```sh
cd Review
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

El resultado se genera como `Review/main.pdf`. Esta fuente usa la clase y el estilo bibliográfico LNCS de Springer: `llncs.cls` y `splncs04.bst`. Esos archivos deben estar disponibles en la instalación local de TeX Live y no se incluyen en este repositorio. En Arch Linux se pueden instalar con:

```sh
sudo pacman -S --needed texlive-publishers
```

## Requisitos

- **LaTeX:** TeX Live con `latexmk`, `pdflatex` y BibTeX, además de los paquetes requeridos por cada documento.
- **LNCS:** clase y estilo Springer disponibles localmente para compilar `Review/`.
- **Python:** Python 3 y las bibliotecas indicadas para ejecutar los scripts de diagnóstico de `Tesis/datos/`.
- **Datos:** el CSV SIPCOP incluido para los scripts que lo procesan. El descargador SIDPOL necesita conexión al servicio ArcGIS externo.

La tesis y la revisión tienen dependencias LaTeX distintas. Compila cada una desde su carpeta para que se resuelvan correctamente las rutas relativas de capítulos, bibliografía, datos y figuras.

## Limpieza de archivos generados

`latexmk` crea archivos auxiliares de LaTeX junto a los fuentes. Para limpiarlos sin borrar los archivos fuente, entra en la carpeta del documento correspondiente y ejecuta:

```sh
latexmk -C
```

Esto elimina también el PDF generado por esa compilación; vuelve a compilar para crearlo de nuevo. Los PDF, CSV descargados y figuras generadas deben añadirse al control de versiones solo si se desea conservar y distribuir explícitamente esos productos.
