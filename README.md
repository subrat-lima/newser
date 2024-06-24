# newser
newser is short for news-scaper

## description 
this tool extracts news headlines and outputs them in json/sfeed format

## options
* `--format:` selects the output format of the news data. supported values are `json` and `sfeed`(default)
* `--save:` saves the file in the specified location

## usage
```py
python newser.py --format=sfeed --save=/file/to/save <url>
```

## updates
* added initial version of the tool to fetch data from odishatv.in

## attribution
built using:
* [selectolax](https://github.com/rushter/selectolax)
* [httpx](https://github.com/encode/httpx)

