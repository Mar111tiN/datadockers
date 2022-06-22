FROM ubuntu:focal
ARG TARGETPLATFORM
ARG USER="martin"

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -yq --no-install-recommends wget bzip2 locales ca-certificates git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV HOME /home/$USER

RUN mkdir $HOME

ENV CONDA_VERSION=4.12.0 \
    PYTHON_VERSION=py39

RUN case "${TARGETPLATFORM}" in \
        "linux/amd64") CONDA_MD5=7843dd7d0a2c53b0df37ca8189672992 ;; \
        "linux/arm64") CONDA_MD5=9baf936183f3479c97bff16fe62fb56c ;; \
    esac \ 
    && printf "TARGETPLATFORM ${TARGETPLATFORM}" \
    && printf "MD5: ${CONDA_MD5}" \
    && wget -q https://repo.anaconda.com/miniconda/Miniconda3-${PYTHON_VERSION}_${CONDA_VERSION}-$(uname -s)-$(uname -mm).sh -O ~/miniconda.sh && \
    echo ${CONDA_MD5} ~/miniconda.sh | md5sum -c - && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Install Tini
RUN conda install --quiet --yes -c conda-forge 'tini=0.19.0' && \
    conda clean --all -f -y

COPY .condarc $HOME

WORKDIR $HOME

ENTRYPOINT [ "tini", "-g", "--" ]
CMD [ "/bin/bash" ]