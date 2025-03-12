import sys
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import argostranslate.translate
from tqdm import tqdm

def traducir_texto(texto, from_lang='en', to_lang='es'):
    return argostranslate.translate.translate(texto, from_lang, to_lang)

def traducir_epub(archivo_entrada, archivo_salida, from_lang='en', to_lang='es'):
    # Cargar libro EPUB
    libro = epub.read_epub(archivo_entrada)

    # Crear nuevo libro traducido
    libro_traducido = epub.EpubBook()
    
    # Recuperar título y autor si están disponibles
    metadata_title = libro.get_metadata('DC', 'title')
    title_str = metadata_title[0][0] if metadata_title else "Libro Traducido"
    libro_traducido.set_title(title_str + ' (Traducido)')
    
    libro_traducido.set_language(to_lang)
    
    metadata_creator = libro.get_metadata('DC', 'creator')
    creator_str = metadata_creator[0][0] if metadata_creator else "Autor desconocido"
    libro_traducido.add_author(creator_str)

    # Definir etiquetas a omitir (por ejemplo, código)
    etiquetas_omitir = {'script', 'style', 'code', 'pre'}

    items = list(libro.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    
    # Barra de progreso para capítulos
    for item in tqdm(items, desc="Procesando capítulos", unit="capítulo"):
        soup = BeautifulSoup(item.get_content(), features='html.parser')
        
        # Obtener todos los nodos de texto
        text_nodes = soup.find_all(text=True)
        
        # Barra de progreso para cada nodo de texto dentro del capítulo
        for nodo in tqdm(text_nodes, desc="Traduciendo nodos", leave=False, unit="nodo"):
            if nodo.parent.name in etiquetas_omitir:
                continue
            texto_original = nodo.strip()
            if texto_original:
                try:
                    texto_traducido = traducir_texto(texto_original, from_lang, to_lang)
                    nodo.replace_with(texto_traducido)
                except Exception as e:
                    print(f"Error al traducir '{texto_original}': {e}")
                    continue

        # Crear capítulo traducido
        capitulo_traducido = epub.EpubHtml(
            uid=item.get_id(),
            title=item.get_name(),
            file_name=item.get_name(),
            lang=to_lang,
            content=str(soup)
        )
        libro_traducido.add_item(capitulo_traducido)

    # Copiar imágenes y otros recursos
    for item in libro.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            libro_traducido.add_item(item)

    # Mantener la estructura del libro
    libro_traducido.toc = libro.toc
    libro_traducido.spine = libro.spine

    # Añadir navegación
    libro_traducido.add_item(epub.EpubNcx())
    libro_traducido.add_item(epub.EpubNav())

    # Guardar el libro traducido
    epub.write_epub(archivo_salida, libro_traducido)

def main():
    if len(sys.argv) < 2:
        print("Uso: python traductor.py <archivo_entrada.epub>")
        sys.exit(1)
    
    archivo_entrada = sys.argv[1]
    if not os.path.exists(archivo_entrada):
        print(f"El archivo {archivo_entrada} no existe.")
        sys.exit(1)
    
    # Generar el nombre del archivo de salida añadiendo '_espanol' antes de la extensión
    base, ext = os.path.splitext(archivo_entrada)
    archivo_salida = f"{base}_espanol{ext}"
    
    print("Iniciando traducción, esto puede tardar unos minutos...")
    traducir_epub(archivo_entrada, archivo_salida)
    print(f"¡Traducción completa! Libro guardado en: {archivo_salida}")

if __name__ == '__main__':
    main()
