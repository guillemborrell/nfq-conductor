#!/bin/sh
# chkconfig: 2345 20 80
# description: Nfq Conductor service

. /etc/init.d/functions

start() {
    echo -n "Starting nfq-conductor..."
    echo
    daemon --pidfile=/var/run/nfq-conductor.pid /usr/local/bin/nfq-conductor --log-file-prefix=/var/log/nfq-conductor&
}

stop() {
    echo -n "Shutting down nfq-conductor..."
    kill -9 `ps aux | grep nfq-conductor | grep -v bash | grep -v /bin/sh | grep -v grep | awk '{print $2}'`
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