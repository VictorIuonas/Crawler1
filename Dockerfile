FROM python:3.7

WORKDIR /usr/src/app

ARG input_config

COPY $input_config "input.json"
COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD scrapy crawl search_repos -a config_file='input.json'; cp output.json /output_dir
