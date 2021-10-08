FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PATH="${PATH}:/root/.local/bin"

RUN apt update && apt -y upgrade && apt install -y netcat postgresql-client\
 python3-setuptools && pip install pipenv

RUN mkdir /app
WORKDIR /app/
COPY . .
RUN pipenv install --system --deploy --skip-lock

# run entrypoint.sh
RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["sh", "./entrypoint.sh"]