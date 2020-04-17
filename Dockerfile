FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache git

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./markdown-to-confluence.py --api_url https://scriveab.atlassian.net/wiki/rest/api/ --title "some title" --path ./git README.md
