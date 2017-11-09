FROM centos:7

RUN yum -y update

RUN yum install -y gcc

RUN yum install -y \
    git \
    curl \
    vim \
    wget \
    make \
    scl-utils \
    centos-release-scl-rh \
    python27

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python2.7 get-pip.py

WORKDIR /
RUN mkdir moonbbs
ADD . /moonbbs/

WORKDIR /moonbbs/
RUN pip install -r /root/pform-kms/requirements.txt

EXPOSE 5000

CMD ["python", "./moonbbs_spider/server.py"]
