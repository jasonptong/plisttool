import json

f = open('plisttool-output-1649004569.638497.json')
genre_data = json.load(f)

print([*genre_data])

count = 1

with open('plisttool-visited.txt', 'a') as f:
    for item in [*genre_data]:
        if genre_data[item]['NSUserTrackingUsageDescription'] is not None:
            print(count)
            count += 1
        f.write("%s\n" % item)