# FROM base.registry-ci.delta.sbrf.ru/base/redhat.io/ubi8/ubi:8.7
FROM redhat.registry-ci.delta.sbrf.ru/ubi8/python-311

USER 0

RUN cat /etc/resolv.conf

# General image set up

ADD https://nexus.sigma.sbrf.ru/nexus/content/repositories/OAIR_tool_release/cert/SberCARootExt.crt /etc/pki/ca-trust/source/anchors/
RUN update-ca-trust

ARG SBEROSC_TOKEN
ARG NEXUS_USERNAME
ARG NEXUS_PASSWORD

RUN echo -e "\
[ubi-8-appstream] \n\
name=ubi-8-appstream \n\
baseurl=https://sberosc.sigma.sbrf.ru/repo/rpm/ubi/dist/ubi8/8/x86_64/appstream/os \n\
enabled=1 \n\
gpgcheck=0 \n\
repo_gpgcheck=0 \n\
username=token \n\
password=${SBEROSC_TOKEN} \n\
 \n\
[ubi-8-baseos] \n\
name=ubi-8-baseos \n\
baseurl=https://sberosc.sigma.sbrf.ru/repo/rpm/ubi/dist/ubi8/8/x86_64/baseos/os \n\
enabled=1 \n\
gpgcheck=0 \n\
repo_gpgcheck=0 \n\
username=token \n\
password=${SBEROSC_TOKEN}" > /etc/yum.repos.d/ubi.repo



RUN dnf repolist --all -v --disableplugin=subscription-manager

# RUN dnf install --allowerasing --nobest -y --nodocs --disableplugin=subscription-manager \
#          git

WORKDIR /opt/sast-manager

RUN mkdir /var/log/sast-manager

# RUN adduser tuz --uid 1001
RUN chown -R 1001:0 /tmp && \
    chmod -R g=u /tmp

RUN chown -R 1001:0 /var && \
    chmod -R g=u /var

RUN chown -R 1001:0 /opt/sast-manager && \
    chmod -R g=u /opt/sast-manager

# RUN mkdir /.ssh
# RUN chown -R 1001:0 /.ssh && \
#     chmod -R g=u /.ssh

USER 1001

RUN python3 -m venv .venv
RUN python3 -m venv .venv_deepsecrets

RUN echo -e "\
[global] \n\
index-url = https://token:${SBEROSC_TOKEN}@sberosc.sigma.sbrf.ru/repo/pypi/simple \n\
extra_index_url=https://${NEXUS_USERNAME}:${NEXUS_PASSWORD}@nexus-ci.delta.sbrf.ru/repository/pypi-dev/simple/ \n\
trusted-host = sberosc.sigma.sbrf.ru nexus-ci.delta.sbrf.ru \n\
default-timeout = 180" > .venv/pip.conf

COPY requirements.txt requirements.txt

RUN .venv/bin/python -m pip install --no-cache-dir -r requirements.txt


COPY src src
COPY entrypoint.py entrypoint.py
# COPY log.ini log.ini
COPY bin bin

# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

ENTRYPOINT [".venv/bin/python", "entrypoint.py"]