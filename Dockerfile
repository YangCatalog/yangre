FROM python:3.10-bullseye
ARG YANG_ID
ARG YANG_GID
ARG YANGLINT_VERSION

ENV YANG_ID "$YANG_ID"
ENV YANG_GID "$YANG_GID"
ENV YANGLINT_VERSION "$YANGLINT_VERSION"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/yangre
ENV PYTHONPATH=$VIRTUAL_ENV/bin/python
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN groupadd -g ${YANG_GID} -r yang && useradd --no-log-init -r -g yang -u ${YANG_ID} -d $VIRTUAL_ENV yang
RUN pip install virtualenv && virtualenv --system-site-packages $VIRTUAL_ENV && mkdir -p /etc/yangcatalog

RUN apt-get -y update
RUN apt-get -y install libxml2 gunicorn rsyslog systemd wget clang cmake libpcre2-dev git

# Install yanglint
RUN cd /home && git clone -b ${YANGLINT_VERSION} --single-branch --depth 1 https://github.com/CESNET/libyang.git
RUN cd /home/libyang && mkdir build
RUN cd /home/libyang/build && cmake .. && make && make install

RUN rm -rf /var/lib/apt/lists/*

COPY . $VIRTUAL_ENV
COPY config.py-dist $VIRTUAL_ENV/config.py
COPY requirements.txt .
RUN pip install -r requirements.txt

# Setup w3cgrep
RUN mkdir -p /home/w3cgrep
COPY w3cgrep.c /home/w3cgrep/.
RUN cd /home/w3cgrep && clang w3cgrep.c -I /usr/include/libxml2 -lxml2 -o /usr/local/bin/w3cgrep
RUN mkdir -p /home/yang/w3cgrep/
RUN cp /usr/local/bin/w3cgrep /home/yang/w3cgrep/

RUN mkdir /var/run/yang
RUN sed -i "/imklog/s/^/#/" /etc/rsyslog.conf
RUN chown -R yang:yang /var/run/yang
RUN chown -R yang:yang $VIRTUAL_ENV

# Support arbitrary UIDs as per OpenShift guidelines

WORKDIR $VIRTUAL_ENV

CMD chown -R yang:yang /var/run/yang && service rsyslog start && /yangre/bin/gunicorn wsgi:application -c gunicorn.conf.py
