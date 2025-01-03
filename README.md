# eBirdDigest
Script to create a digest of local birds to see based on recent eBird observations.

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
