"""Logging configuration module. """

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logging_basic(
        level,
        format,
        file_handler: Optional[bool] = False
    ):
    """
    Utilizza basicConfig logging con parametri passati.
    Imposta anche un file handler (opzionale, con rollover su 5 file di log).
    """

    logging.basicConfig(level=level, format=format)
    
    if file_handler:
        fh = RotatingFileHandler("logs/app.log", maxBytes=10_000_000, backupCount=5)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(format))
        logging.getLogger().addHandler(fh)


# Esegui subito la configurazione
logger_name = "web3_fastapi"
info_lvl = logging.INFO
fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

setup_logging_basic(
    level=info_lvl,
    format=fmt,
    file_handler=False
)
# Esporta logger dedicato
logger = logging.getLogger(logger_name)
