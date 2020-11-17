FROM library/ubuntu:20.04

ENV MINIFORGE_VERSION=4.8.2-1
ENV CONDA_DIR=/opt/conda

# Apt Packages
RUN apt-get update --fix-missing \
    && apt-get install wget -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Miniforge
# https://github.com/ContinuumIO/docker-images/issues/140
RUN URL="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" \
    && INSTALLER="miniforge.sh" \
    && wget --quiet $URL -O /tmp/${INSTALLER}  \
    && /bin/bash /tmp/${INSTALLER} -b -p ${CONDA_DIR} \
    && ${CONDA_DIR}/bin/conda init bash \
    && rm /tmp/${INSTALLER}

COPY environment.yaml /tmp/environment.yaml
RUN /opt/conda/bin/conda env create -f /tmp/environment.yaml

ENV UID=1000
ENV USER=ubuntu
ENV PATH="/opt/conda/envs/jupyterhub/bin/:$PATH"

RUN groupadd --gid ${UID} ${USER}  \
    && useradd --create-home --gid ${UID} --no-log-init --shell /bin/bash --uid ${UID} ${USER} \
    && ln -s ${CONDA_DIR}/etc/profile.d/conda.sh /etc/profile.d/conda.sh

USER ubuntu
WORKDIR /home/ubuntu

CMD ["jupyterhub", "--config", "/opt/jupyterhub_config.py"]