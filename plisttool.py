from file_helper import exists,file_ext, new_filename
from plists import get_plists_by_genre

import argparse
import datetime

ct = datetime.datetime.now()
ts = ct.timestamp()

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=lambda s:file_ext("txt", s, parser), 
                    help="File containing bundle IDs for native iOS")
parser.add_argument("attributes", type=lambda s:file_ext("txt", s, parser),
                    help="List of plist attributes")
parser.add_argument("-v", "--visited", type=lambda s:file_ext("txt", s, parser),
                    help="File containing a list of bundle IDs to skip")
parser.add_argument("-o", "--output", type=lambda s:file_ext("json", s, parser), nargs='?', default="plisttool-output-%s.json" % (str(ts)),
                    help="Output file")
parser.add_argument("-u", "--email", type=str, nargs='?', default='',
                    help="Apple ID email")
parser.add_argument("-p", "--password", type=str, nargs='?', default='',
                    help="Apple ID password")
args = parser.parse_args()

bundles = new_filename(args.filename)
if not exists(bundles):
    parser.error("File %s does not exist" % (bundles))

attributes = new_filename(args.attributes)
if not exists(attributes):
    parser.error("File %s does not exist" % (attributes))

if args.visited:
    visited = new_filename(args.visited)
    if not exists(visited):
        parser.error("File %s does not exist" % (visited))
else:
    visited = None

output = new_filename(args.output)

get_plists_by_genre(bundles, attributes, visited, output, args.email, args.password)





