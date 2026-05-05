# Podcast Kanazawa

Podcast personal generado estáticamente y servido via GitHub Pages.

## Cómo funciona

Este proyecto usa un generador estático para crear un feed RSS compatible con Apple Podcasts y una página web minimalista para escuchar los episodios. Todo se automatiza con GitHub Actions.

### Arquitectura

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  GitHub         │     │   GitHub     │     │  GitHub     │
│  Releases       │────▶│   Repo       │────▶│  Pages      │
│  (audio + img)  │     │  (episodios) │     │  (RSS+Web)  │
└─────────────────┘     └──────────────┘     └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  GitHub      │
                        │  Actions     │
                        │  (generador) │
                        └──────────────┘
```

1. **Subís el audio** (`.m4a`) como asset de un **GitHub Release** en este mismo repo.
2. **Creás un archivo Markdown** en `episodes/` con los metadatos del episodio (título, fecha, link al release, etc.).
3. **Hacés `git push`** a la rama `main`.
4. **GitHub Actions** corre `generate.py`, que:
   - Lee todos los episodios de la carpeta `episodes/`
   - Genera el feed RSS (`feed.xml`) compatible con Apple Podcasts
   - Genera la página web (`index.html`) con reproductor de audio
5. **GitHub Pages** sirve los archivos generados automáticamente.

### Formato del feed RSS

El feed sigue la especificación RSS 2.0 con el namespace de iTunes (`<itunes:*>`), que es lo que Apple Podcasts necesita para leer el podcast correctamente. Cada episodio incluye:

- Título y descripción
- Fecha de publicación (formato RFC-822)
- GUID único
- Enclosure con URL directa al audio, tamaño y tipo MIME (`audio/mp4` para `.m4a`)
- Duración
- Imagen opcional

### Por qué GitHub Releases

**GitHub Releases** es la forma más simple y confiable de hostear archivos de audio para un podcast personal:

- ✅ **URLs permanentes**: `https://github.com/usuario/repo/releases/download/vX.Y.Z/archivo.m4a`
- ✅ **Sin límites de ancho de banda** para repos públicos
- ✅ **CORS habilitado**: funciona en navegadores y apps de podcast
- ✅ **Sin autenticación**: cualquiera puede descargar
- ✅ **Ya tenés GitHub**: no necesitás otra cuenta ni servicio

> **Nota**: Cuando un usuario accede a la URL, GitHub redirige a una URL temporal de Azure Blob Storage. Esto es transparente tanto para navegadores como para agregadores de podcasts.

## Agregar un episodio

### 1. Crear un GitHub Release con el audio

1. Andá a la pestaña **Releases** de tu repo en GitHub.
2. Clic en **Draft a new release**.
3. Elegí una etiqueta de versión (ej: `v1.0.0`, `v1.1.0`).
4. Título: nombre del episodio.
5. En **Attach binaries**, arrastrá tu archivo `.m4a`.
6. Publicá el release.
7. Copiá la URL del asset. Se ve así:
   ```
   https://github.com/kanazawa-dev/personal-podcast/releases/download/v1.0.0/episodio-pressman.m4a
   ```

### 2. Crear el archivo del episodio

Crear un archivo `episodes/YYYY-MM-DD-titulo-del-episodio.md`:

```markdown
---
title: "Episodio 1 - El principio"
date: 2026-05-04
duration: "42:15"
audio_url: "https://github.com/kanazawa-dev/personal-podcast/releases/download/v1.0.0/episodio-pressman.m4a"
audio_size: 58346917
image_url: "https://github.com/kanazawa-dev/personal-podcast/releases/download/v1.0.0/cover-episodio.jpg"
---

Descripción del episodio. Puede ser tan larga como quieras.
Puede incluir markdown básico como **negrita** o [links](https://ejemplo.com).
```

**Campos:**

| Campo | Requerido | Descripción |
|-------|-----------|-------------|
| `title` | Sí | Título del episodio |
| `date` | Sí | Fecha de publicación (formato `YYYY-MM-DD`) |
| `duration` | Sí | Duración del audio (`HH:MM:SS` o `MM:SS`) |
| `audio_url` | Sí | Link de compartir de Google Drive al archivo `.m4a` |
| `audio_size` | No | Tamaño aproximado en bytes (ayuda al lector de RSS) |
| `image_url` | No | Link de compartir de Google Drive a una imagen de portada del episodio |

**Imagen del episodio:**
- Subila como asset del mismo GitHub Release donde está el audio
- Formatos recomendados: `.jpg` o `.png`
- Tamaño recomendado: 1400x1400px (mínimo 600x600px para iTunes)
- Si no especificás `image_url`, el episodio usa la imagen general del podcast definida en `config.yml`

### 3. Publicar

```bash
git add .
git commit -m "Agregado episodio 1"
git push origin main
```

GitHub Actions se encarga del resto. En 1-2 minutos el episodio aparece en:
- La web: `https://kanazawa-dev.github.io/personal-podcast`
- El feed RSS: `https://kanazawa-dev.github.io/personal-podcast/feed.xml`

## Configuración general

Editá `config.yml` para cambiar los datos del podcast:

```yaml
title: "Podcast Kanazawa"
description: "Un podcast sobre tecnología, desarrollo y lo que me cruza por la cabeza."
author: "Alex Elgueta"
language: "es"
email: "podcast@kanazawa.dev"
category: "Technology"
explicit: "no"
base_url: "https://kanazawa-dev.github.io/personal-podcast"
image: "https://kanazawa-dev.github.io/personal-podcast/cover.jpg"
```

- `image`: URL de la imagen de portada general del podcast. Se muestra en Apple Podcasts como carátula principal. Idealmente 1400x1400px o 3000x3000px.
- `category`: Categoría para iTunes. Ver [lista de categorías de Apple](https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12).

## Suscribirse en el iPhone

1. Abrí la app **Podcasts**.
2. Andá a **Biblioteca** > **Editar** > **Añadir programa por URL**.
3. Pegá la URL del feed:
   ```
   https://kanazawa-dev.github.io/personal-podcast/feed.xml
   ```
4. Tocá **Suscribirse**.

## Migrar a otro hosting de audio

Si en algún momento querés dejar de usar GitHub Releases (por ejemplo, si necesitás más de 2GB por archivo o querés analytics de reproducción):

1. Subí tus audios a otro servicio (Cloudflare R2, AWS S3, Backblaze B2, etc.).
2. Obtené URLs directas y permanentes a los archivos.
3. En cada archivo de episodio en `episodes/`, cambiá el campo `audio_url` por la nueva URL.
4. Hacé `git push`.

El resto del sistema funciona exactamente igual. No hay que tocar nada del generador.

## Estructura del proyecto

```
personal-podcast/
├── config.yml              # Configuración general del podcast
├── episodes/               # Un archivo .md por episodio
│   └── 2026-05-04-episodio-de-ejemplo.md
├── templates/
│   ├── feed.xml            # Plantilla RSS
│   └── index.html          # Plantilla web
├── generate.py             # Generador estático (Python + Jinja2)
├── .github/workflows/
│   └── deploy.yml          # CI/CD para GitHub Pages
├── public/                 # Generado automáticamente (no editar manualmente)
│   ├── feed.xml
│   └── index.html
└── README.md               # Este archivo
```

## Desarrollo local

Para probar cambios en el generador o templates antes de pushear:

```bash
# Instalar dependencias
pip install jinja2 pyyaml

# Generar feed y web localmente
python generate.py

# Ver el resultado
cat public/feed.xml
cat public/index.html
```

## Troubleshooting

### Error "XML mal formado" en el feed

Si ves un error de XML al abrir el feed, probablemente haya un carácter especial sin escapar en algún episodio (como `&`, `<`, `>` en la descripción o título). El generador usa `autoescape` de Jinja2 para evitar esto, pero si editás manualmente el XML, asegurate de escapar estas entidades.

### Drive muestra una página de advertencia en lugar del audio

Esto pasa cuando se descarga el mismo archivo muchas veces desde la misma IP en poco tiempo. Soluciones:
- Esperá unas horas y volvé a intentar
- Migrá el archivo a otro hosting (R2, S3, etc.)
- Para uso personal, esto raramente es un problema

### El episodio no aparece en Apple Podcasts

- Verificá que el feed sea XML válido abriéndolo en el navegador
- Asegurate de que el campo `pubDate` tenga una fecha válida (formato RFC-822)
- Revisá que la URL del `enclosure` sea accesible directamente (no una página intermedia)

## Créditos

Generado con un sistema estático custom usando Python, Jinja2 y GitHub Actions. Inspirado en la simplicidad de los generadores de sitios estáticos como Jekyll y Hugo, pero adaptado específicamente para podcasts.
