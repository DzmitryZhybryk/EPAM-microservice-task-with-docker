FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/master"
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /master

EXPOSE 5000

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "./app.py"]
