import logging

def setup_logging(filename):
        
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=logging.INFO,
        filename=filename,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
