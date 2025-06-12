from govee_control import reset_all_strips
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - [API] - %(levelname)s: %(message)s',  # Custom format
    datefmt='%H:%M:%S'  # Display only hour, minute, and second
)
log = logging.getLogger("ICS")

reset_all_strips()