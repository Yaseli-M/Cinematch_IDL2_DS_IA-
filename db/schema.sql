-- Esquema de Base de Datos - Cinematch

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'usuario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    genero TEXT NOT NULL,
    duracion INTEGER NOT NULL,
    violencia TEXT NOT NULL,
    lenguaje_ofensivo TEXT NOT NULL,
    romance TEXT NOT NULL,
    animacion TEXT NOT NULL,
    rating TEXT NOT NULL,
    anio_estreno INTEGER NOT NULL,
    publico_objetivo_real TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predicciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    pelicula_id INTEGER,
    genero TEXT NOT NULL,
    duracion INTEGER NOT NULL,
    violencia TEXT NOT NULL,
    lenguaje_ofensivo TEXT NOT NULL,
    romance TEXT NOT NULL,
    animacion TEXT NOT NULL,
    rating TEXT NOT NULL,
    anio_estreno INTEGER NOT NULL,
    publico_objetivo_predicho TEXT NOT NULL,
    confianza REAL,
    fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE SET NULL
);
