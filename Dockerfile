from ubuntu:18.04

ENV VIM_DEV=1 DEBIAN_FRONTEND=noninteractive \
    PATH="~/miniconda3/bin:${PATH}"  \
    TERM=xterm-256color 
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -y \
    ca-certificates \
    sudo \
    git \
    x11-apps \
    wget \
    ttf-dejavu \
    --no-install-recommends 
    #&& \
    #rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/mmorse1217/terraform --recursive

WORKDIR /terraform 
RUN bash dotfiles/setup.sh 

RUN bash programs/python.sh 

# build vim
RUN bash vim/build_from_source.sh  

RUN bash vim/lang-servers/setup.sh  
ENV PATH /root/miniconda3/bin:$PATH
RUN bash vim/lang-servers/python-language-server.sh  

# install plugins
RUN bash vim/install_plugins.sh



RUN conda install -y nose matplotlib ipython jupyter numpy scipy
RUN pip install jupyter
WORKDIR /src
CMD ["/bin/bash"]

#WORKDIR /root
