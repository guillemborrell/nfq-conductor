Quick start
===========

Running the simplest setup in a single computer is as easy as launching the conductor
process::

    $> nfq-conductor

and the daemon::

    $> nfq-conductor-daemon

Thanks to some serious magic, the order is not important. You can then visit
the conductor GUI in http://localhost:8888.

There are three ways of running a process with the conductor. The first one
is using the wrapper::

    $> nfq-runner --command ls

This will redirect the output of the standard output and standard error to the
conductor. The logs will be available at the web GUI and through the RESTful
api::

    $> curl localhost:8888/api/last/10
    [{"source": "c7872c40-0556-40da-be42-8fae17f49200", "when": (...)

The task runs locally, but the output is sent to the conductor for storage and
visualization. We can also send the same command through the GUI.

.. note::

   At this point of the development, the GUI may undergo substantial changes.
   This documentation will therefore omit references on how to use conductor
   this way. In any case, the web GUI will be very easy to use.

The third way in which a command, or a set of commands can be submitted to the
daemons connected to the conductor.

Configuring the conductor in cluster of servers
-----------------------------------------------

It's kind of obvious, but you only need a conductor, and you have to run a daemon
at each server you want to make available to the conductor. Since it is probable
that the server where the conductor is running may have multiple interfaces,
the simplest way of getting it up and running is the following:

    $> nfq-conductor --collector=tcp://your.ip.for.workers:port

There are other options to configure the storage for the logs. The default is
that all the logs are erased every time you shut down the conductor. You must
make the daemons aware of where the conductor is running, therefore the
``collector`` option must be present when starting the daemon as well.

    $> nfq-collector-daemon --collector=tcp://your.ip.for.workers:port --interface=eth0

Run as much daemons as worker nodes and you will have a cluster up and running.