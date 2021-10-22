import logging
import sys

def init_logger():
    """
    Initialize logging.
    @Returns: Logger object
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    global stdout_handler
    formatter = logging.Formatter('%(asctime)s - %(name)s '
                                  '- %(levelname)s - %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)
    root.addHandler(stdout_handler)
