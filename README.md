# plisttool

This tool uses the [ipatool](https://github.com/majd/ipatool) to download .ipa files. Apple ID email and password are needed in order to bypass app certificate requests.

**Guide**

Retrieve a list of bundle ids based on genre.

```
usage: genre.py [-h] [-o [OUTPUT]] [-l [LIMIT]]

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Output file containing bundle IDs for native iOS
  -l [LIMIT], --limit [LIMIT]
                        The maximum amount of search results to retrieve (default: 5)
```

Retrieve plist attribute(s) from bundle ids.
```
usage: plisttool.py [-h] [-v VISITED] [-o [OUTPUT]] [-u [EMAIL]]
                    [-p [PASSWORD]]
                    filename attributes

positional arguments:
  filename              File containing bundle IDs for native iOS
  attributes            List of plist attributes

optional arguments:
  -h, --help            show this help message and exit
  -v VISITED, --visited VISITED
                        File containing a list of bundle IDs to skip
  -o [OUTPUT], --output [OUTPUT]
                        Output file
  -u [EMAIL], --email [EMAIL]
                        Apple ID email
  -p [PASSWORD], --password [PASSWORD]
                        Apple ID password
```
