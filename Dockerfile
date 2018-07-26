FROM centos:latest

#MAINTAINER uestc <wuaicjg@163.com>

#ADD shell.tar /
#ADD requests-2.13.0.tar /
#ADD scapy-2.3.2.tar /
#ADD setuptools-0.6c11-py2.7.egg /
ADD ["requests-2.13.0.tar", "scapy-2.3.2.tar", "setuptools-0.6c11-py2.7.egg", "pip-9.0.1.tar.gz", "/"]
RUN set -ex \
    && yum install -y tcpdump nmap gcc snmp \
    && cd / \
    && sh setuptools-0.6c11-py2.7.egg \
    && cd /scapy-2.3.2 \
    && python setup.py install \
    && cd /requests-2.13.0 \
    && python setup.py install \
    && cd /pip-9.0.1 \
    && python setup.py install \
    && yum clean all

ADD ["shell/", "/"]

CMD python detect.py
