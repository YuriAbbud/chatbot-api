import logging

def setup_logging(filename):
    logging.basicConfig(
        level=logging.INFO,
        filename=filename,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
