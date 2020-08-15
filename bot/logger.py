import logging


formatter = logging.Formatter("{asctime} - {levelname} - {message} - "
                              "module: {module} - function: {funcName} - "
                              "line: {lineno}", datefmt="%D - %H:%M:%S",
                              style="{")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# console stream_handler
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.DEBUG)

log.addHandler(console)


