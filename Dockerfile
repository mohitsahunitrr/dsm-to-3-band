FROM ubuntu:18.04

# Install basic things
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y build-essential

# Install language
RUN apt install -y python python-pip python-gdal gdal-bin libgdal-dev

# Set an user for app
RUN useradd -m dsm-to-color-scale

WORKDIR /home/dsm-to-color-scale

ENTRYPOINT ["/bin/bash"]
