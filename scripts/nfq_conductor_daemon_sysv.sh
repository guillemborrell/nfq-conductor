#!/bin/sh
# chkconfig: 2345 20 80
# description: Nfq Conductor daemon

. /etc/init.d/functions

start() {
    echo -n "Starting nfq-conductor-daemon..."
    echo
    daemon --pidfile=/var/run/nfq-conductor-daemon.pid /usr/local/bin/nfq-conductor-daemon --uuid=worker_0 --log-file-prefix=/var/log/nfq-conductor-daemon&
}

stop() {
    echo -n "Shutting down nfq-conductor-daemon..."
    kill -9 `ps aux | grep nfq-conductor-daemon | grep -v bash | grep -v /bin/sh | grep -v grep | awk '{print $2}'`
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)

        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage:  {start|stop|status|restart}"
        exit 1
        ;;
esac
exit $?
