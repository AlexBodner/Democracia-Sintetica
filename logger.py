import logging
import textwrap
import os

# --- Configuración del Logger (lo que ya tienes) ---
logger = logging.getLogger("debate_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("debate_system.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# --- Clase personalizada para formatear el mensaje ---
class WrappedFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', wrap_width=None):
        super().__init__(fmt, datefmt, style)
        self.wrap_width = 100

    def format(self, record):
        original_message = record.getMessage()
        # Envuelve el mensaje si es necesario
        wrapped_message = "\n".join(textwrap.wrap(original_message, width=self.wrap_width, subsequent_indent="    "))
        record.msg = wrapped_message  # Sobreescribe el mensaje del record
        return super().format(record)

# --- Aplicar el formateador personalizado al StreamHandler ---
# Puedes aplicar esto solo al console_handler si quieres que el archivo mantenga la línea larga
# O puedes crear un segundo formateador con un ancho muy grande para el file_handler.
wrapped_console_formatter = WrappedFormatter(
    fmt='[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    wrap_width=80- len('[YYYY-MM-DD HH:MM:SS] [LEVEL] NAME - ') # Ajusta para el prefijo del log
)
console_handler.setFormatter(wrapped_console_formatter)
