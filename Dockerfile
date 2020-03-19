from ubuntu:18.04

RUN apt-get update && \ 
    apt-get install --no-install-recommends -y wget \
    bzip2 \
    x11-apps \
    vim && \
    rm -rf /var/lib/apt/lists/*

# install anaconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    echo 'export PATH="/root/miniconda3/bin:$PATH"' | cat - ~/.bashrc > /tmp/out \
    &&  mv /tmp/out ~/.bashrc && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH /root/miniconda3/bin:$PATH

RUN conda install -y nose matplotlib ipython jupyter 
