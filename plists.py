from queries import get_ids

from collections import defaultdict
from pathlib import Path
import atexit
import datetime
import json
import os
import plistlib
import re
import shutil
import subprocess
import tempfile
import zipfile


# This has to be run on macOS, because it relies on `plutil(1)` to convert binary Info.plist files
# into ASCII xml plist files. If you know the Info.plist will not be binary, you should be able to
# run this on other systems with minimal modification

# we pass the file path of the .ipa and array of plist keys to retrieve
# returns: a dict of the plist keys and their values as found in the app’s Info.plist
def get_attritubes_from_ipa(ipa_file, attributes):
    retval = {}
    
    try:
        zip_archive = zipfile.ZipFile(ipa_file, 'r')
    except zipfile.BadZipFile:
        return retval
    
    # we want Payload/{filename}.app/Info.plist, but we have to find the value for {filename}.app
    app_filename = ''
    p = re.compile('Payload/[^/]+\\.app/$')
    for file_info in zip_archive.infolist():
        if p.match(file_info.filename):
            # TODO: regex saved subpattern match may be clearer than this basename/dirname nonsense
            app_filename = os.path.basename(os.path.dirname(file_info.filename))
            break
    
    if app_filename == '':
        raise ValueError('Supplied zip file (`%s`) did not contain an entry matching `Payload/*.app`' % ipa_file)
    
    plist_relpath = 'Payload/%s/Info.plist' % app_filename
    temp_dir = tempfile.mkdtemp() # extract the plist to here
    
    # wrap this all in a try, so that we can clean up the temp dir we made in case of failure
    try:
        zip_archive.extract(plist_relpath, temp_dir)
        extracted_plist_abspath = '%s/%s' % (temp_dir, plist_relpath)
        
        # convert what may be a binary plist to an xml plist so that python’s plistlib can use it
        # see the man page for plutil(1) for more on plutil
        retcode = subprocess.check_call(['/usr/bin/plutil', '-convert', 'xml1', extracted_plist_abspath])
        with open(extracted_plist_abspath, 'rb') as f:
            plistObj = plistlib.load(f)
        for attr in attributes:
            if attr in plistObj:
                retval[attr] = plistObj[attr]
            else:
                retval[attr] = None
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise
        
    shutil.rmtree(temp_dir)
    return retval

'''
def get_plists_by_genre(genres, attributes, limit=5, output_dir=Path().absolute(), **kwargs):
    visited = []
    email = ''
    password = ''
    for key, value in kwargs.items():
        if key == 'v':
            with open(value, 'r') as f:
                visited = [bundle_id.rstrip() for bundle_id in f]
        elif key == 'e':
            email = value
        elif key == 'p':
            password = value

    ct = datetime.datetime.now()
    ts = ct.timestamp()
    ipa_folder = "plisttool-ipa-%s" % (str(ts))
    os.system("mkdir " + ipa_folder)

    output_json = {}
    output_file = "%s/plisttool-output-%s.json" % (output_dir, str(ts))

    def exit_handler(ipa_folder, output_file, output_json):
        with open(output_file, 'w') as fp:
            json.dump(output_json, fp, sort_keys=True, indent=4, default=str)
        fp.close()
        os.rmdir(ipa_folder)

    atexit.register(exit_handler, ipa_folder, output_file, output_json)

    for genre in genres:
        ids_info = get_ids(genre, limit)
        for id_info in ids_info:
            if '{http://itunes.apple.com/rss}id' in id_info:
                bundle_id = id_info['{http://itunes.apple.com/rss}bundleId']
                if bundle_id not in visited:
                    visited.append(bundle_id)
                    subprocess.run(["ipatool", "download", "-b", bundle_id, "-o", ipa_folder + "/"])
                    ipa_file = os.listdir(ipa_folder)
                    if len(email) > 0 and len(password) > 0 and not os.listdir(ipa_folder):
                        subprocess.run(["ipatool", "auth", "login", "-e", email, "-p", password])
                        subprocess.run(["ipatool", "download", "-b", bundle_id, "-o", ipa_folder + "/", "--purchase"])
                    if not os.listdir(ipa_folder):
                        continue
                    ipa_file = os.listdir(ipa_folder)
                    abs_path = '%s/%s' % (ipa_folder, ipa_file[0])
                    plist_dict = get_attritubes_from_ipa(abs_path, attributes)
                    if not plist_dict:
                        continue
                    output_json[bundle_id] = plist_dict
                    os.remove(abs_path)
'''

def get_plists_by_genre(bundles_file, attributes_file, visited_file, output, email, password, output_dir=Path().absolute()):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    ipa_folder = "plisttool-ipa-%s" % (str(ts))
    os.system("mkdir " + ipa_folder)

    output_json = {}
    if not output:
        output_file = "%s/plisttool-output-%s.json" % (output_dir, str(ts))
    else:
        output_file = output

    def exit_handler(ipa_folder, output_file, output_json):
        with open(output_file, 'w') as fp:
            json.dump(output_json, fp, sort_keys=True, indent=4, default=str)
        fp.close()
        os.rmdir(ipa_folder)

    atexit.register(exit_handler, ipa_folder, output_file, output_json)

    bundle_ids = []
    with open(bundles_file, 'r') as f:
        bundle_ids = [b.rstrip() for b in f]
    f.close()

    attributes = []
    with open(attributes_file, 'r') as f:
        attributes = [a.rstrip() for a in f]
    f.close()

    visited = []
    if visited_file:
        with open(visited_file, 'r') as f:
            visited = [v.rstrip() for v in f]
        f.close()

    for bundle_id in bundle_ids:
        if bundle_id not in visited:
            visited.append(bundle_id)
            subprocess.run(["ipatool", "download", "-b", bundle_id, "-o", ipa_folder + "/"])
            ipa_file = os.listdir(ipa_folder)
            if len(email) > 0 and len(password) > 0 and not os.listdir(ipa_folder):
                subprocess.run(["ipatool", "auth", "login", "-e", email, "-p", password])
                subprocess.run(["ipatool", "download", "-b", bundle_id, "-o", ipa_folder + "/", "--purchase"])
            if not os.listdir(ipa_folder):
                continue
            ipa_file = os.listdir(ipa_folder)
            abs_path = '%s/%s' % (ipa_folder, ipa_file[0])
            plist_dict = get_attritubes_from_ipa(abs_path, attributes)
            if not plist_dict:
                continue
            output_json[bundle_id] = plist_dict
            os.remove(abs_path)



