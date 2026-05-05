# Personal Podcast

Podcast personal generado estáticamente y servido via GitHub Pages.

## Cómo funciona

1. Agregás un archivo Markdown en `episodes/` con los metadatos del episodio.
2. Subís el audio (`.m4a`) a Google Drive y copiás el link compartido.
3. Hacés `git push` a la rama `main`.
4. GitHub Actions corre `generate.py`, crea el RSS (`feed.xml`) y la web (`index.html`), y los publica automáticamente.

## Pasos para usar Drive (por ahora)

1. Subí tu `.m4a` a Google Drive.
2. Clic derecho > **Compartir** > **Cambiar a "Cualquiera con el enlace"**.
3. Copiá el link. Se ve así:
   ```
   https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing
   ```
4. En el archivo del episodio, pegalo en el campo `audio_url`. El generador lo convierte automáticamente al formato directo.

> ⚠️ **Limitación de Drive**: si bajás el mismo archivo muchas veces en poco tiempo, Google puede devolver una página de advertencia en lugar del audio. Para uso personal es raro que pase, pero si escalás, migrá a Cloudflare R2 o similar (cambias la URL y listo).

## Agregar un episodio

Crear `episodes/YYYY-MM-DD-titulo.md`:

```markdown
---
title: "Episodio 1 - El principio"
date: 2026-05-04
duration: "42:15"
audio_url: "https://drive.google.com/file/d/TU_ID/view?usp=sharing"
audio_size: 20480000
---

Descripción del episodio. Puede ser tan larga como quieras.
```

- `duration`: formato `HH:MM:SS` o `MM:SS`.
- `audio_size`: tamaño aproximado en bytes (no es crítico, pero ayuda).

## Configurar GitHub Pages

1. Andá a **Settings > Pages** del repo.
2. En **Build and deployment** seleccioná **GitHub Actions**.
3. La primera vez que hagas push a `main`, se va a deployar automáticamente.

## Suscribirse en el iPhone

1. Abrí la app **Podcasts**.
2. Andá a **Biblioteca > Editar > Añadir programa por URL**.
3. Pegá la URL del feed:
   ```
   https://tunombredeusuario.github.io/personal-podcast/feed.xml
   ```

## Migrar audio a otro hosting

Cuando quieras dejar de usar Drive, solo cambiá el campo `audio_url` de cada episodio por la URL directa de tu nuevo hosting (R2, S3, Backblaze, etc.). El resto del sistema sigue igual.
