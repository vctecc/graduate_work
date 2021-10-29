FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PATH="${PATH}:/root/.local/bin"

RUN apt update && apt -y upgrade && apt install -y python3-setuptools\
 netcat && pip install pipenv

RUN mkdir /app
WORKDIR /app/
COPY Pipfile /app/

RUN pipenv install --system --deploy --skip-lock
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0", "--workers", "4"]