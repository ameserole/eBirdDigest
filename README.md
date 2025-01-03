# eBirdDigest
Script to create a digest of local birds to see based on recent eBird observations. Generates a HTML report page that contains a potential list of lifers and all notable birds seen within the provided locations in the last day. Along with each sighting a link to the eBird trip report and a Google Maps URL with either just the coordinates provided or directions if a home address was provided. If emailDigest is set the HTML report will be sent using the to/from parameters. 

## Usage
```
 python3 ./ebird_query.py --help
usage: ebird_query.py [-h] --eBirdApi EBIRDAPI [--lifers LIFERS] [--outputFile OUTPUTFILE] --locations LOCATIONS
                      [LOCATIONS ...] [--homeAddress HOMEADDRESS] [--emailDigest] [--emailTo EMAILTO]
                      [--emailFrom EMAILFROM]

options:
  -h, --help            show this help message and exit
  --eBirdApi EBIRDAPI   File with eBird API Key
  --lifers LIFERS       File with list of bird IDs to filter out of observations list
  --outputFile OUTPUTFILE
                        File to write HTML output
  --locations LOCATIONS [LOCATIONS ...]
                        List of eBird location codes to query
  --homeAddress HOMEADDRESS
                        Home Address to use when creating Google Maps URL
  --emailDigest         Send email digest
  --emailTo EMAILTO     Email to line
  --emailFrom EMAILFROM
                        Email from line
```

## Requirements
To run the digest generator you will need your own eBird API key. Go to https://ebird.org/api/keygen to generate your own. To automatically email the digest you will need to setup a gmail account with API access and run through the authentication flow yourself.  
  
For the list of eBird bird IDs see: https://science.ebird.org/en/use-ebird-data/the-ebird-taxonomy  
For the list of eBird location IDs see: https://ebird.org/explore

