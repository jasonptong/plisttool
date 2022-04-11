from file_helper import file_ext, new_filename
from queries import get_genre_bundle_ids

from PyInquirer import style_from_dict, Token, prompt, Separator

import argparse
import datetime
import json
import os
import sys

ct = datetime.datetime.now()
ts = ct.timestamp()

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=lambda s:file_ext("txt", s, parser), nargs='?', default="plisttool-bundle-ids-%s.txt" % (str(ts)),
                    help="Output file containing bundle IDs for native iOS")
parser.add_argument("-l", "--limit", type=int, nargs='?', default=5,
                    help="The maximum amount of search results to retrieve")
args = parser.parse_args()

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

choices = [Separator('= Top iOS App Store Genres =')]
choices.append({
    'name': 'ALL'
})
ids = []
id_mapping = {}

f = open(os.path.join(sys.path[0],'top_genres.json'))
genre_data = json.load(f)

for genre in genre_data['genres']:
    choices.append({'name': genre['name']})
    id_mapping[genre['name']] = genre['genreId']
    ids.append(genre['genreId'])


questions = [
    {
        'type': 'checkbox',
        'message': 'Genre Encoding',
        'name': 'genres',
        'choices': choices,
        'validate': lambda answer: '' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)

id_answer = []

if 'ALL' in answers['genres']:
    id_answer.extend(ids)

for genre in answers['genres']:
    if genre != 'ALL':
        id_ = id_mapping[genre]
        if id_ in id_answer:
            id_answer.remove(id_)
        else:
            id_answer.append(id_)

output_file = new_filename(args.output)
get_genre_bundle_ids(id_answer, output_file, args.limit)