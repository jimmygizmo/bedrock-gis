FROM quay.io/jupyter/minimal-notebook:latest

# Custom settings like dark them as default
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

# TODO: Attempting to customize Jupyter Lab tab title. This did not work. Check target dir path.
## Create the standard labconfig directory - for custom page config
#RUN mkdir -p /etc/jupyter/labconfig
## Custom page config; e.g. title - copy in the file
#COPY page_config.json /etc/jupyter/labconfig/page_config.json


# Copy requirements and install
COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r /tmp/requirements.txt


WORKDIR /home/bedrock/workspace


EXPOSE 8888


# By default starts Jupyter Lab. Classic Notebook is also available.
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]

