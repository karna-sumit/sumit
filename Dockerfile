FROM python:3-slim

COPY ./src ./src


RUN pip3 install -r src/requirements.txt

WORKDIR /src

ENTRYPOINT [ "python3" ]

CMD [ "warehouse_inventory.py" ]