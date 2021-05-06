# _Cowin Status Tracker_
These script allow you to view available vaccination slots for a pincode or district.

### Usage
`python district.py <districtname>`

OR

`python pincode.py <pincode>`

Note: For *nix systems, replace `python` with `python3`.

These script will fetch status automatically every 10 minutes and display it on terminal. To exit the script, just press `Ctrl + C`.

**Important note for district.py**

If the district name has multiple words, it needs to be written as "district name" (for Windows) or 'district name' (for *nix). Otherwise " " or ' ' are optional.

For Windows:
`python district.py "East Delhi"`

For *nix:
`python3 district.py 'East Delhi'`

### Dependency
These script use some external libraries which can be installed using pip.

For Windows:
`pip install -r requirements.txt`

For *nix:
`pip3 install -r requirements.txt`
