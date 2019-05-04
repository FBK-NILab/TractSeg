FROM neurodebian:stretch-non-free

MAINTAINER Pietro and Paolo (from Soichi Hayashis <hayashis@iu.edu>)

ENV DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && apt-get install -y git g++ python python-numpy libeigen3-dev zlib1g-dev libqt4-opengl-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev fsl-complete python-pip jq strace curl vim 
RUN apt-get update && apt-get install -y apt-utils git g++ libeigen3-dev zlib1g-dev libqt4-opengl-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev fsl-complete jq strace curl vim wget

## install conda
ENV PATH /opt/conda/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda2-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN conda install numpy

#libgomp1 seems to comes with pytorch so I don't need it

#RUN pip install --upgrade pip

## install and compile mrtrix3
#RUN git clone https://github.com/MRtrix3/mrtrix3.git
#RUN cd mrtrix3 && git fetch --tags && git checkout tags/3.0_RC3 && ./configure && ./build
#ENV PATH=$PATH:/mrtrix3/bin

RUN mkdir -p ~/.tractseg \
    && mkdir -p /code \
    && curl -SL -o /code/mrtrix3_RC3.tar.gz \
       https://zenodo.org/record/1415322/files/mrtrix3_RC3.tar.gz?download=1
RUN tar -zxvf /code/mrtrix3_RC3.tar.gz -C code \
    && /code/mrtrix3/set_path

#RUN pip install seaborn
#RUN pip install torch torchvision
RUN conda install -c anaconda seaborn

## NVIDIA CUDA Installation
###########################
# LICENSE:
##########
# Copyright (c) 2017, NVIDIA CORPORATION. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of NVIDIA CORPORATION nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# BASE INSTALLATION
###################
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates apt-transport-https && \
    rm -rf /var/lib/apt/lists/* && \
    NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +2 > cudasign.pub && \
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

ENV CUDA_VERSION 9.1.85

ENV CUDA_PKG_VERSION 9-1=$CUDA_VERSION-1
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-$CUDA_PKG_VERSION && \
    ln -s cuda-9.1 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.1"


# RUNTIME INSTALLATION
######################
ENV NCCL_VERSION 2.2.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
    libnccl2=$NCCL_VERSION-1+cuda9.1 && \
    apt-mark hold libnccl2 && \
    rm -rf /var/lib/apt/lists/*


# CUDNN INSTALLATION
####################
ENV CUDNN_VERSION 7.1.2.21
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn7=$CUDNN_VERSION-1+cuda9.1 && \
    apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*


RUN conda install pytorch torchvision cudatoolkit=9.0 -c pytorch

#install batchgenerator/tractseg
#RUN pip install https://github.com/MIC-DKFZ/batchgenerators/archive/master.zip \
#    && pip install https://github.com/MIC-DKFZ/TractSeg/archive/v1.7.1.zip
RUN git clone https://github.com/MIC-DKFZ/batchgenerators.git \
    && cd batchgenerators \
    && git checkout 34980972009516a27e2b99837a4f483ce280cf9a \
    && pip install . \
    && cd ..
    
RUN git clone https://github.com/FBK-NILab/TractSeg-BrainLife.git \
    && cd TractSeg-BrainLife \
    && git checkout brainlife-app \
    && pip install . \
    && cd ..
     
#RUN HOME=/ download_all_pretrained_weights

#make it work under singularity 
RUN ldconfig && mkdir -p /N/u /N/home /N/dc2 /N/soft

#https://wiki.ubuntu.com/DashAsBinSh 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
