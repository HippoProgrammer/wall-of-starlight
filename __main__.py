# import modules
import requests, json, os, subprocess, sys, argparse, logging, shlex
from requests_sse import EventSource, InvalidStatusCodeError, InvalidContentTypeError

# create logger
logger = logging.getLogger(__name__)

# create arg parser
parser = argparse.ArgumentParser(prog="wall-of-starlight",description="A basic script that walls a NationStates region\"s RMB messages") 
parser.add_argument("-e","--level",default=20)
parser.add_argument("-o","--log",action="store_true")
parser.add_argument("region",default="starlight")
args = parser.parse_args()

# convert parsed args to individual variables
region = str(args.region)
if args.level.isdigit():
    level = int(args.level)
else:
    level = logging.INFO

# set logging level based on parsed args
logger.setLevel(level)

# set up logging to stdout based on parsed args
if args.log:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# define main program
def main():
    logger.warning("Entered main script")
    logger.info("Subscribing to SSE...")
    try:
        with EventSource(f"https://www.nationstates.net/api/region:{region}", timeout=30) as event_source: # subscribe to the SSE feed for the specified region
            try:
                for event in event_source: # for each event supplied by SSE
                    data = json.loads(event.data) # convert the data to a native dictionary
                    if "rmb" in data["buckets"]: # we know the data comes from the region, if it is also an RMB message continue processing
                        logger.info("RMB event received")
                        
                        # get nation data
                        nation = "someone"
                        for bucket in data["buckets"]: 
                             if "nation:" in bucket:
                                 nation = bucket.split(':')[1]
                        nation_repr = repr(nation)
                        logger.debug(f"Nation repr: {nation_repr}")

                        # check for nation error cases and log
                        if nation == "someone":
                            logger.warning(f"Nation is still set as {nation}. This almost certainly means that fetching nation name from SSE feed has failed. Core message functionality may still be unaffected.")

                        # get message data
                        message = data["rmbMessage"]
                        message_repr = repr(message)
                        logger.debug(f"Message repr (pre-escaping): {message_repr}")

                        # escape message data to supported format
                        message = message.replace("\r\n", " ") # escape CRLF to spaces for one-line output
                        message = message.replace(r'"', "'") # escape double quotes by replacing them with single quotes
                        message = message.replace(r"`", "'") # escape backticks by replacing them with single quotes
                        message_repr = repr(message)
                        logger.debug(f"Message repr (post-escaping): {message_repr}")

                        # construct output based on data
                        output = f"wall-of-starlight says: New message from {region}! :3 \\| {nation} says: \"{message}\""
                        output_repr = repr(output)
                        logger.debug(f"Output repr: {output_repr}")
                        
                        # send output to TTYs using Unix 'wall' command
                        try:
                            subprocess.run(["wall", output], check=True)
                        except subprocess.CalledProcessError:
                            logger.error("Wall command returned non-zero status command. TTY support is inoperative.")
                        logger.info("Walled RMB message for all TTYs")

                        # send output to pTTYs using Unix /dev/pts files
                        for file in os.listdir("/dev/pts/"):
                            if file.isdigit(): # filters for numerical pTTYs only
                                subprocess.run(f"echo {output} >/dev/pts/{file}", shell=True, check=True)
                                logger.info(f"Wrote RMB message to /dev/pts for pTTY {file}")
                    else:
                        logger.info("Non-RMB event received, ignoring")
            except InvalidStatusCodeError:
                logger.error('Invalid status code received from SSE feed.')
            except InvalidContentTypeError:
                logger.error('Invalid content received from SSE feed.')
            except requests.RequestException:
                logger.error('Generic error in requesting data from SSE feed.')
    except KeyboardInterrupt:
        logger.warning("Exiting main script")

# final checks before beginning program
if os.name != "posix": # if ran on non-Unix-based system
    logger.error("Program ran on non-Unix-based system, and as such all features are unsupported. Run this program on a Unix-based OS. Exiting")
elif __name__ != "__main__": # if imported as module
    logger.error("Program imported as module, and as such all features are unsupported. Run this program direct from the Python interpreter. Exiting")
else:
    main()
