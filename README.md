![](docs/_static/nfq_solutions.png)

# Conductor helps you to orchestrate the processes running in your cluster.

Conductor provides the following tools

* A web interface for launching, killing and watching the logs of processes. It
  can also send alerts in an asynchronous fashion via websockets (`nfq-conductor`)

* A daemon for every node in the cluster that manages the local processes and
  provides several metrics to the web interface (`nfq-conductor-daemon`)
  
* A process wrapper that captures the standard output of a process (the logs),
  and sends them to the web interface (`nfq-runner`)
  
* A launcher that can configure a cluster of processes at boot time
  (`nfq-conductor-submit`)


## License

The project license is specified in LICENSE.md