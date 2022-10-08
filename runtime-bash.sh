#!/bin/bash
# Some code taken from https://github.com/novnc/noVNC/blob/master/utils/novnc_proxy

die() {
    vncserver -clean -kill :1
    exit 0
}

printf "${VNC_PASSWORD}\n${VNC_PASSWORD}\n\n" | vncpasswd

vncserver :1 -geometry ${VNC_WIDTH}x${VNC_HEIGHT} -depth 24 -name "Stringray-${P_SERVER_UUID}"
echo "VNC server running..."

/opt/websockify/websockify-${WEBSOCKIFY_VERSION}/run ${SERVER_PORT} localhost:5901
proxy_pid="$!"
sleep 1
if ! ps -p ${proxy_pid} >/dev/null; then
    proxy_pid=
    echo "Failed to start WebSockets proxy"
    exit 1
fi

echo "Ready for connection!"

wait ${proxy_pid}
