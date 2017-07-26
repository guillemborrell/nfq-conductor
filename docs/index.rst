Welcome to Conductor's documentation!
=====================================

Assume you have a cluster of some servers. Something in between two and two
thousand of them. You want to send a simple command, like ``ls`` or ``ps aux``
to one of the nodes (or all of them), to capture the output, and to store it
to analyze the output later. This is what Conductor is for.

Assume that you have some processes running in the background and you have
designed a web frontend to check how things are going. This web GUI can obtain
the logs of the different processes using the Conductor RESTful API, and in
case something strange happens, that very same web application can get
alerts using the websockets protocol.

These are just two examples.

Conductor is a simple tool for process orchestration in a cluster of computers.
It provides the following utilities:

* ``nfq-conductor`` web interface for launching, killing and watching logs of
  processes. It can also send alerts via websockets.

* ``nfq-conductor-daemon`` is a small daemon that manages the worker-side
  features of nfq-conductor. Each server running the daemon process will be
  automatically added to the cluster. It also provides some elementary metrics
  to the conductor like CPU or memory usage.

* ``nfq-runner`` is a simple wrapper to launch commands in the command line
  and incorporate them as processes launched with the conductor interface.

* ``nfq-conductor-submit`` is similar to the runner, but it launches a set
  of commands specified as a json file.

The requirements of Conductor are quite standard apart from the fact that
there's no python 2.7 support. Deal with it. Installing is as easy as::

    $> pip install nfq-conductor

Contents:

.. toctree::
   :maxdepth: 2

   quickstart

License
-------

Conductor is released under the AGPL-v3 license.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

