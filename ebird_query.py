from ebird.api import get_observations, get_notable_observations
from gmail_send import gmail_send_message
import sys
import datetime
import argparse
import urllib.parse


api_key = ''
BASE_MAPS_DIR_URL = "https://www.google.com/maps/dir/?api=1&origin={}&destination={},{}&travelMode=driving"
BASE_MAPS_SEARCH_URL = "https://www.google.com/maps/search/?api=1&query={},{}"
BASE_SUB_URL = "https://ebird.org/checklist/{}"


def generateMsg(birds, homeAddress=""):
    message = ""

    message += f"<h2>Total Unique Birds {len(birds.values())}</h2>\n"
    for sightings in birds.values():
        message += f"<h3>{sightings[0]['comName']}:</h3>\n"
        message += '<table style="border: 2px solid #8C8C8C;">\n'
        message += """
            <thead>
                <tr>
                <th scope="col" style="border: 1px solid #0A0A0A;">Date</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">Location</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">Coords</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">Private Location</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">Valid Observation</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">eBird Checklist URL</th>
                <th scope="col" style="border: 1px solid #0A0A0A;">Directions</th>
                </tr>
            </thead>"""
        for sighting in sightings:
            if homeAddress != "":
                mapsUrl = BASE_MAPS_DIR_URL.format(urllib.parse.quote_plus(homeAddress), sighting['coords'][0], sighting['coords'][1])
            else:
                mapsUrl = BASE_MAPS_SEARCH_URL.format(sighting['coords'][0], sighting['coords'][1])
            message += f"""
            <tr>
                <th scope="row" style="border: 1px solid #0A0A0A;">{sighting['obsDt']}</th>
                <td style="border: 1px solid #0A0A0A;">{sighting['locName']}</td>
                <td style="border: 1px solid #0A0A0A;">{sighting['coords'][0]}, {sighting['coords'][1]}</td>
                <td style="border: 1px solid #0A0A0A;">{sighting['locationPrivate']}</td>
                <td style="border: 1px solid #0A0A0A;">{sighting['obsValid']}</td>
                <td style="border: 1px solid #0A0A0A;"><a href="{BASE_SUB_URL.format(sighting['subId'])}">eBird</a></td>
                <td style="border: 1px solid #0A0A0A;"><a href="{mapsUrl}">Maps</a></td>
            </tr>"""

        message += "</table>\n"

    return message


def createBirdRecords(records, lifers=[]):
    birds = {}

    for record in records:
        
        if record['speciesCode'] in lifers:
            continue
        
        if record['speciesCode'] not in birds.keys():
            birds[record['speciesCode']] = []
        
        birds[record['speciesCode']].append(
            {
                'comName': record['comName'],
                'locName': record['locName'],
                'obsDt': record['obsDt'],
                'locId': record['locId'],
                'coords': (record['lat'], record['lng']),
                'locationPrivate': record['locationPrivate'],
                'obsValid': record['obsValid'],
                'subId': record['subId']
            }
        )
    
    return birds


def generateLifers(locations, lifers, homeAddress):
    records = get_observations(api_key, locations, 1, category='species', provisional=True)
    birds = createBirdRecords(records, lifers)
    return generateMsg(birds, homeAddress)


def generateNotables(locations, homeAddress):
    records = get_notable_observations(api_key, locations, 1)
    birds = createBirdRecords(records)
    return generateMsg(birds, homeAddress)

def buildHtml(locations, lifersMsg="", notablesMsg=""):

    htmlBody = "<html>\n"
    htmlBody += "<h1>Digest for Locations: "
    for location in locations:
        htmlBody += f"{location}, "
    
    htmlBody = htmlBody[:-2]
    
    htmlBody += "</h1>\n"

    if lifersMsg != "":
        htmlBody += "<h1>Potential Nearby Lifers:</h1>\n"
        htmlBody += lifersMsg
    
    if notablesMsg != "":
        htmlBody += "<h1>Potential Nearby Notables:</h1>\n"
        htmlBody += notablesMsg
    
    htmlBody += "</html>\n"
    return htmlBody

def main():
    global api_key

    parser = argparse.ArgumentParser()
    parser.add_argument("--eBirdApi", required=True, help="File with eBird API Key")
    parser.add_argument("--lifers", help="File with list of bird IDs to filter out of observations list")
    parser.add_argument("--outputFile", help="File to write HTML output")
    parser.add_argument("--locations", required=True, nargs="+", help="List of eBird location codes to query")
    parser.add_argument("--homeAddress", default="", help="Home Address to use when creating Google Maps URL")
    parser.add_argument("--emailDigest", action="store_true", help="Send email digest")
    parser.add_argument("--emailTo", help="Email to line")
    parser.add_argument("--emailFrom", help="Email from line")
    args = parser.parse_args()

    if not args.emailDigest and not args.outputFile:
        print("One of emailDigest or outputFile needs to be set!")
        sys.exit(-1)

    try:
        api_key = open(args.eBirdApi).read().strip('\n')
    except:
        print("Failed to open API Key File")
        sys.exit(-1)

    if args.lifers:
        try:
            lifers = open(args.lifers).read().split('\n')
        except:
            print("Failed to open Lifers File")
            sys.exit(-1)
    else:
        lifers = []

    lifersMsg = generateLifers(args.locations, lifers, args.homeAddress)
    notablesMsg = generateNotables(args.locations, args.homeAddress)
    fullHtml = buildHtml(args.locations, lifersMsg, notablesMsg)
    
    if args.outputFile:
        try:
            open(args.outputFile, 'w').write(fullHtml)
        except:
            print("Failed to write to output file!")
            sys.exit(-1)

    if args.emailDigest:
        if not args.emailTo or not args.emailFrom:
            print("Email To or Email From not set!")
            sys.exit(-1)
        
        subject = f"eBird Digest {datetime.date.today()}"
        gmail_send_message(args.emailTo, args.emailFrom, subject, fullHtml)
    

if __name__ == '__main__':
    main()

