# Bedrock-GIS, Magma-GIS FastAPI Services
FROM python:3.10.9-slim

WORKDIR /appdir

# wait-for-it.sh pauses FastAPI startup until postgres is listening on its port
COPY ./wait-for-it.sh /appdir/wait-for-it.sh
RUN chmod o+x /appdir/wait-for-it.sh

# Install Linux build tools to enable some Python installations
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Standard upgrades for any Python environment
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# Both type of requirements files are copied. Only one is ever used, depending on dev activity.
COPY requirements-pinned.txt /appdir/
COPY requirements.txt /appdir/

# Install all Python dependencies. (Magma application module installed separately below)
# You ocasionally need to use the non-pinned file to re-generate/update the pinned file using pip freeze.
# Choose your method according to a good plan, at the right time:
# Use requirements-pinned.txt if you are not changing any modules. Use this for production deployment:
RUN #pip install --no-cache-dir -r requirements-pinned.txt
# Use requirements.txt if you are actively changing, updating or adding modules. Use this for dev only (sometimes):
RUN pip install --no-cache-dir -r requirements.txt

# Magma application module package, ready for installation
COPY ./magma/ /appdir/magma/

# Magma application module test suites (PyTest)
COPY ./tests/ /appdir/tests/

# Entrypoint file
COPY ./magmastart.py /appdir/

# setup.py enables pip installation of magma app module
COPY ./setup.py /appdir/

# Install the Bedrock Magma application module
RUN pip install .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "magmastart:app", "--bind", "0.0.0.0:8000"]

