ARG TAG=3.8

FROM martin37szyska/jupyter-minimal:${TAG}-alpine

ARG CURRENTUSER=10151

USER root

# add code_master to the python path and a possibly local folder code to PYTHONPATH
RUN echo "sys.path.insert(0,'/home/martin/code_master')" >> .ipython/profile_default/startup/startup.py && \
    echo "sys.path.insert(0,'/home/martin/work/code')" >> .ipython/profile_default/startup/startup.py

# copy the registry code to code_master
COPY code ${HOME}/code_master

# copy the notebook templates to nb_templates for local use
COPY nb ${HOME}/nb_templates

# Switch back to martin to avoid accidental container runs as root
USER $CURRENTUSER