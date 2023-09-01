FROM python:3.8.12-buster
WORKDIR /prod

# First, pip install dependencies
COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt

# Then only, install solar_panel_status!
COPY solar_panel_status solar_panel_status
COPY setup.py setup.py
RUN pip install .

# We already have a make command for that!
COPY Makefile Makefile
RUN make reset_local_files

#CMD uvicorn taxifare.api.fast:app --host 0.0.0.0

CMD uvicorn solar_panel_status.api.api:app --host 0.0.0.0 --port $PORT
