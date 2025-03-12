# Traductor de EPUB de Inglés a Español

Este proyecto es una herramienta en Python para traducir libros en formato EPUB desde inglés a español, manteniendo la estructura original y omitiendo la traducción de fragmentos de código (etiquetas `<code>` y `<pre>`). El proyecto ofrece dos implementaciones:

1. **Con Argos Translate:**  
   - **Ventajas:** Completamente gratuito y offline.  
   - **Desventajas:** La calidad de la traducción puede ser inferior, especialmente en textos técnicos.

2. **Con MarianMT (Helsinki-NLP/opus-mt-en-es):**  
   - **Ventajas:** Mayor calidad en la traducción, sobre todo para textos técnicos y de programación.  
   - **Desventajas:** Requiere mayor espacio en disco (aproximadamente 300-350 MB) y puede necesitar más recursos de cómputo.

## Requisitos

- Python 3.x  
- [uv](https://github.com/Kozea/uv) para la instalación de dependencias.

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/traductor-epub.git
   cd traductor-epub
   ```

2. **Instala las dependencias comunes:**

   Utiliza `uv` para instalar las siguientes dependencias:

   ```bash
   uv install ebooklib beautifulsoup4 tqdm
   ```

3. **Instala dependencias específicas según la versión que desees usar:**

   - **Para la versión con Argos Translate:**

     ```bash
     uv install argostranslate
     ```

     Luego, instala el modelo de traducción de inglés a español (ejecuta este código una única vez en una consola de Python):

     ```python
     import argostranslate.package
     import argostranslate.translate

     from_code = "en"
     to_code = "es"

     argostranslate.package.update_package_index()
     available_packages = argostranslate.package.get_available_packages()

     package_to_install = next(
         filter(
             lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
         )
     )
     argostranslate.package.install_from_path(package_to_install.download())
     ```

   - **Para la versión con MarianMT:**

     ```bash
     uv install transformers
     ```

## Uso

El programa se ejecuta desde la línea de comandos pasando como argumento el archivo EPUB que se desea traducir. El archivo de salida se genera automáticamente agregando `_espanol` antes de la extensión.

### Ejemplos de Ejecución

- **Con Argos Translate:**

  ```bash
  python traductor_argos.py libro_en_ingles.epub
  ```

- **Con MarianMT:**

  ```bash
  python traductor_marian.py libro_en_ingles.epub
  ```

## Funcionalidad

- **Omisión de código:**  
  Los fragmentos de código en etiquetas `<code>` y `<pre>` se omiten durante la traducción.

- **Barras de progreso:**  
  Se utiliza `tqdm` para mostrar el progreso en el procesamiento de capítulos y nodos de texto.

- **Conservación de la estructura:**  
  Se preservan imágenes, estilos y otros recursos del EPUB original.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, abre un _issue_ o envía un _pull request_ en el repositorio.

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

---

¡Disfruta traduciendo tus libros y facilitando el acceso a contenidos en múltiples idiomas!
