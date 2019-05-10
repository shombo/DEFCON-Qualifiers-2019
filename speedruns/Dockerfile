FROM ubuntu@sha256:d26d529daa4d8567167181d9d569f2a85da3c5ecaf539cace2c6223355d69981

RUN echo 'export LC_CTYPE=C.UTF-8' >> /root/.bashrc
RUN echo 'export LD_LIBRARY_PATH=/usr/local/lib/' >> /root/.bashrc
RUN apt update && apt install -y python-pip gdb wget python3-pip vim cmake git
RUN pip install pwntools
RUN pip3 install keystone-engine unicorn capstone ropper pyvex archinfo z3
RUN cp /usr/local/lib/python3.6/dist-packages/usr/lib/python3/dist-packages/keystone/libkeystone.so /usr/local/lib/
RUN wget -q -O- https://github.com/hugsy/gef/raw/master/scripts/gef.sh | sh
WORKDIR /mnt

ENTRYPOINT "/bin/bash"
