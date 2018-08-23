import logging

formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("scraper.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logging.basicConfig(
    format=formatter,
    level=logging.DEBUG,
    handlers=[
        stream_handler,
        file_handler
    ]
)

def get_logger():
    return logging
