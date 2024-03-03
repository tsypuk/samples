FROM alpine as builder
WORKDIR /

MAINTAINER Roman Tsypuk
# Set metadata for the image
LABEL maintainer="Roman Tsypuk<tsypuk.rb@gmail.com>"

ENV SYSBENCH_VER=1.0.20
ADD https://github.com/akopytov/sysbench/archive/${SYSBENCH_VER}.tar.gz .
RUN apk add --update alpine-sdk git linux-headers automake autoconf libtool libaio-dev openssl-dev libunwind-dev mysql-dev
RUN tar -xf ${SYSBENCH_VER}.tar.gz && \
	cd sysbench-${SYSBENCH_VER} && \
	export TARGET_LIBS=-lunwind;./autogen.sh && \
	./configure && \
	make -j && \
	make DESTDIR=/sysbench/sysbench-install-root/ install

FROM alpine as benchmark
MAINTAINER Roman Tsypuk
# Set metadata for the image
LABEL maintainer="Roman Tsypuk<tsypuk.rb@gmail.com>"


# sysbench
RUN apk add --update --no-cache so:libgcc_s.so.1 so:libmariadb.so.3 so:libaio.so.1
RUN apk update
RUN apk add sysbench
# speedtest
RUN apk add speedtest-cli
RUN apk add mc
RUN apk add aws-cli

WORKDIR /
CMD mkdir results
ADD benchmark.py .

# container without process - only for benchmarking
CMD tail -f /dev/null