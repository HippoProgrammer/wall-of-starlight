import requests, json, os, sys, argparse, logging
from requests_sse import EventSource, InvalidStatusCodeError, InvalidContentTypeError

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog="wall-of-starlight",description="A basic script that walls a NationStates region\"s RMB messages")
parser.add_argument("-e","--level",default=20)
parser.add_argument("-o","--log",action="store_true")
parser.add_argument("region",default="starlight")
args = parser.parse_args()

if args.level:
    logger.setLevel(args.level)

if args.log:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(args.level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    logger.info("Started")
    region = str(args.region)
    
    logger.info("Subscribing to SSE...")
    try:
        with EventSource(f"https://www.nationstates.net/api/region:{region}", timeout=30) as event_source: # subscribe to the SSE feed for the specified region
            try:
                for event in event_source: # for each event supplied by SSE
                    logger.info("New event")
                    data = json.loads(event.data) # convert the data to a native dictionary
                    if "rmb" in data["buckets"]: # we know the data comes from the region, if it is also an RMB message continue processing
                        logger.info("RMB event received")
                        nation = "someone"
                        for bucket in data["buckets"]: # we need to fetch the nation
                             if "nation:" in bucket:
                                 nation = bucket.split(':')[1]
                        message = f"wall-of-starlight says: New message from {region}! :3 | {nation} says \"" + str(data["rmbMessage"]) + "\"!" # get the string representation of the message
                        os.system(f"wall {message}")
                        logger.info("Walled RMB message")
                        for file in os.listdir("/dev/pts/"):
                            if file.isdigit(): # filters for numerical pttys only
                                logger.info(f"Echoed RMB message to /dev/pts for pTTY {file}")
                                os.system(f"echo \"{message}\" >/dev/pts/{file}")
            except InvalidStatusCodeError:
                pass
            except InvalidContentTypeError:
                pass
            except requests.RequestException:
                pass
    except KeyboardInterrupt:
        logger.info("Stopped")
        sys.exit()

if __name__ == "__main__":
    main()
