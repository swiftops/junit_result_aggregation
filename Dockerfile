FROM python:3-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7973

CMD [ "python", "services.py" ]