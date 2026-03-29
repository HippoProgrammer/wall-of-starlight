import requests, json, os, argparse
from requests_sse import EventSource, InvalidStatusCodeError, InvalidContentTypeError

parser = argparse.ArgumentParser(prog='wall-of-starlight',description='A basic script that walls a NationStates region\'s RMB messages')
parser.add_argument('region')
args = parser.parse_args()

region = str(args.region)

with EventSource(f"https://www.nationstates.net/api/region:{region}", timeout=30) as event_source: # subscribe to the SSE feed for the specified region
    try:
        for event in event_source: # for each event supplied by SSE
            data = json.loads(event.data) # convert the data to a native dictionary
            if "rmb" in data["buckets"]: # we know the data comes from the region, if it is also an RMB message continue processing
                message = data["rmbMessage"] # get the string representation of the message
                print(message)
                os.system(f"wall {message}")
    except InvalidStatusCodeError:
        pass
    except InvalidContentTypeError:
        pass
    except requests.RequestException:
        pass
