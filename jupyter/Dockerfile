# Choose your desired base image
FROM jupyter/datascience-notebook:latest

# Create a Python 2.x environment using conda including at least the ipython kernel
# and the kernda utility. Add any additional packages you want available for use
# in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 ipython ipykernel kernda pip && \
    conda clean -tipsy

USER root

# Create a global kernelspec in the image and modify it so that it properly activates
# the python2 conda environment.
RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
$CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json

USER $NB_USER

# Automatically install python modules when requirements.txt changes
RUN $CONDA_DIR/envs/python2/bin/pip install when-changed

# Load environment variables from python
RUN $CONDA_DIR/envs/python2/bin/pip install python-dotenv

# Generate the Jupyter Notebook configuration
RUN jupyter notebook --generate-config

# Set up the password from the environment
ARG JUPYTER_PASSWORD
ENV JUPYTER_PASSWORD=$JUPYTER_PASSWORD
COPY ./setup.py /setup.py
RUN $CONDA_DIR/envs/python2/bin/easy_install hashlib
RUN $CONDA_DIR/envs/python2/bin/python /setup.py

WORKDIR .jupyter/
