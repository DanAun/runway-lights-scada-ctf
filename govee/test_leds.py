import logging
import time
import govee_control as gc

# Set up logging with a custom format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

ICS_log = logging.getLogger("ICS")
ICS_log.setLevel(logging.WARN)

def main():
    log.info("Starting LED testing script.")
    
    # Reset all LED strips
    log.info("Resetting all LED strips.")
    gc.reset_all_strips()
    
    # Test each LED strip
    for i in range(1,gc.MAX_TEAM_NUM+1):
        gc.activate_team_light(i)
        log.info("Light for team %d activated. Please check if it is lit up.", i)
        time.sleep(0.5)

    log.info("LED testing completed. Please ensure all LEDs are functioning properly.")

if __name__ == "__main__":
    main()
