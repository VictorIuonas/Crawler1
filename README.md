# Crawl GitHub for Red Points

Crawler for GitHub Links from repositories/issues/wikis search result pages

## Getting Started

Clone this repositories.


### Running

Create an input.json following this struture:

{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}

Run the following two commands:

docker build -t mycrawler --build-arg input_config=input.json . <br />
docker run -v $(pwd):/output_dir mycrawler <br />


