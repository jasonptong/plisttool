from pathlib import Path
from xml.etree.ElementTree import fromstring, ElementTree
import requests

def get_ids(genre, limit=5):
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topfreeapplications/sf=143441/limit=%s/genre=%s/xml' % (limit, genre)
    document = requests.get(url)

    tree = ElementTree(fromstring(document.content))
    root = tree.getroot()

    return [child.attrib for child in root.iter('{http://www.w3.org/2005/Atom}id')]

def get_genre_bundle_ids(genres, filename, limit, output_dir=Path().absolute()):
    #output_file = "%s/%s" % (output_dir, filename)
    bundle_ids = []
    for genre in genres:
        ids_info = get_ids(genre, limit)
        for id_info in ids_info:
            if '{http://itunes.apple.com/rss}id' in id_info:
                bundle_ids.append(id_info['{http://itunes.apple.com/rss}bundleId'])
        print("%s: %s" % (genre, len(ids_info) - 1))
    bundle_ids = list(set(bundle_ids))
    with open(filename, 'w') as file:
        for bundle_id in bundle_ids:
            file.write("%s\n" % (bundle_id))
