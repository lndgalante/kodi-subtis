# Subtis Subtitles (Kodi)

Addon de servicio de subtítulos para Kodi que usa la API de [Subtis](https://subtis.io) para buscar y descargar subtítulos en español automáticamente.

## Requisitos

- Kodi 19+ (Matrix) con xbmc.python 3.0.0
- Conexión a internet

## Instalación

1. Descarga el ZIP del addon (release o paquete generado localmente).
2. En Kodi: **Add-ons** → **Instalar desde archivo ZIP** → selecciona el ZIP.
3. Espera la notificación de instalación exitosa.

### Empaquetado manual (si clonas el repo)

1. Crea una carpeta `service.subtitles.subtis`.
2. Copia dentro `addon.xml`, `service.py`, `README.md` y `resources/`.
3. Comprime la carpeta en un ZIP manteniendo la estructura de raíz.

## Uso

1. Reproduce una película en Kodi.
2. Abre el menú de subtítulos (tecla `T` o desde el OSD).
3. Selecciona **Subtis** como proveedor.
4. El subtítulo se descarga y aplica automáticamente.

**Nota:** series/TV shows aún no están soportados.

## Cómo funciona

### Estrategia de búsqueda

La búsqueda se hace en cascada hasta encontrar una coincidencia:

1. **Hash del video (OpenSubtitles)**
2. **Tamaño en bytes**
3. **Nombre exacto del archivo**
4. **Búsqueda alternativa (fuzzy)**

Si la coincidencia viene de la búsqueda alternativa, Kodi marca el subtítulo como **no sincronizado**.

### Acciones del addon

| Acción     | Descripción                                               |
|------------|-----------------------------------------------------------|
| `search`   | Busca subtítulos para el archivo en reproducción           |
| `download` | Descarga el subtítulo desde `subtitle_link`               |

### API Endpoints

Base URL: `https://api.subt.is/v1`

| Endpoint | Uso |
|----------|-----|
| `GET /subtitle/find/file/hash/{hash}` | Coincidencia por hash del video |
| `GET /subtitle/find/file/bytes/{bytes}` | Coincidencia por tamaño en bytes |
| `GET /subtitle/find/file/name/{filename}` | Coincidencia exacta por nombre |
| `GET /subtitle/file/alternative/{filename}` | Coincidencia difusa por nombre |

**Respuesta exitosa (200):**
```json
{
  "subtitle": {
    "subtitle_link": "https://...",
    "subtitle_file_name": "Movie.Name.2024.srt"
  },
  "title": {
    "title_name": "Movie Name",
    "year": "2024"
  }
}
```

### Almacenamiento

Los subtítulos descargados se guardan temporalmente en:
```
{kodi_profile}/addon_data/service.subtitles.subtis/temp/
```

## Estructura del repositorio

```
.
├── addon.xml          # Manifest del addon
├── service.py         # Lógica principal
├── README.md          # Documentación
└── resources/
    └── icon.png       # Icono del addon
```

## Desarrollo

### Logs

Los logs del addon usan el prefijo `### SUBTIS ###`. Puedes verlos en:

- **Kodi** → **Sistema** → **Registro** (habilitar debug).
- Archivo de log (según SO):
  - Windows: `%APPDATA%\Kodi\kodi.log`
  - Linux: `~/.kodi/temp/kodi.log`
  - macOS: `~/Library/Logs/kodi.log`

Ejemplo de log:
```
### SUBTIS ### Search requested but no media is playing
### SUBTIS ### ERROR: No subtitles found or API error (status: 404)
```

### Publicación

Antes de publicar, actualiza la versión en `addon.xml`:
```xml
<addon id="service.subtitles.subtis" version="X.Y.Z" ...>
```

## Troubleshooting

| Problema | Solución |
|----------|----------|
| "No hay reproducción activa" | Asegúrate de que hay una película reproduciéndose |
| "Película no encontrada" | El archivo no está en la base de datos de Subtis |
| "Soporte para series proximamente" | Las series aún no están soportadas |
| Subtítulo no aparece | Revisa los logs para ver errores de red o API |

## Limitaciones actuales

- Solo películas (no series/episodios).
- Solo subtítulos en español.
- Subtítulos alternativos pueden no estar perfectamente sincronizados.
