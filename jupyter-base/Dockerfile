ARG TAG=3.8

FROM martin37szyska/miniconda:${TAG}-alpine

USER root

ARG USER=martin

ENV HOME=/home/${USER}

RUN mkdir ${HOME}/work

WORKDIR $HOME

RUN chmod 777 ${HOME}/work

RUN conda install --quiet --yes \
    'notebook==6.0.3' && \
    conda clean --all -f -y

EXPOSE 8888

USER  10151

WORKDIR $HOME

CMD ["/opt/conda/bin/jupyter", "notebook", "--ip='*'",  "--no-browser", "--notebook-dir=."]