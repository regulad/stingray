FROM        --platform=$TARGETOS/$TARGETARCH python:3.6-slim-buster

LABEL       author="Parker Wahle" maintainer="regulad@regulad.xyz"

LABEL       org.opencontainers.image.source="https://github.com/regulad/stingray"
LABEL       org.opencontainers.image.licenses=GPL-3.0

ENV 		WEBSOCKIFY_VERSION 0.10.0
ENV         DEBIAN_FRONTEND noninteractive
ENV 		DESKTOP :1
ENV			DISPLAY :1

RUN         apt update && apt upgrade -y \
				&& apt install -y gcc g++ libgcc1 lib32gcc1 libc++-dev gdb libc6 git wget curl tar zip unzip binutils xz-utils liblzo2-2 cabextract iproute2 net-tools netcat telnet libatomic1 libsdl1.2debian libsdl2-2.0-0 \
    			libfontconfig libicu63 icu-devtools libunwind8 libssl-dev sqlite3 libsqlite3-dev libmariadbclient-dev libduktape203 locales ffmpeg gnupg2 apt-transport-https software-properties-common ca-certificates tzdata \
    			liblua5.3 libz-dev rapidjson-dev \
				tigervnc-standalone-server tigervnc-common \
				xfce4 xfce4-goodies \
				firefox-esr libreoffice \
				&& update-locale lang=en_US.UTF-8 \
				&& dpkg-reconfigure --frontend noninteractive locales \
				&& useradd -m -d /home/container -s /bin/bash -u 988 container

RUN 		mkdir -p /opt/websockify \
    			&& curl -SL https://github.com/novnc/websockify/archive/refs/tags/v$WEBSOCKIFY_VERSION.tar.gz \
    			| tar xzC /opt/websockify

RUN			echo "allowed_users = anybody" | tee -a /etc/X11/Xwrapper.config

RUN 		python -m pip install 'numpy<1.17' redis simplejson jwcrypto

USER        container
ENV         USER=container HOME=/home/container
WORKDIR     /home/container

COPY        ./entrypoint.sh /entrypoint.sh
CMD         [ "/bin/bash", "/entrypoint.sh" ]
