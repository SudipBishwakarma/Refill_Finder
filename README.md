# Refill-Finder

Refill-Finder is a demo app which makes use of Google Sheets Python API and jQuery for DOM manipulation. This app reads data from multiple sheets in a single spreadsheet and then generates individual json files so as to use it in an interactive pen refill finder webpage.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python). Follow their documentation to get API credentials.

```bash
$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Usage
Place the files in your webserver document root. Generate products.json and brands.json with command below
```bash
$ python3 refill_finder.py
```

Visit interactive refill-finder page on local machine
```bash
http://localhost/refill_finder
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
You are free to use this app and do whatever you want with it.
