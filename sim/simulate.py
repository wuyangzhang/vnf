'''
the simulator to simulate the VNF scheduling and packet processing
'''

import simpy

'''
how to write a simulator?


@network topology?
topology zoo
Jisc network 
link capacity: random?

@server topology?
skip...


@server capacity?
# data center. random number 100 - 500 VMs
set the percentage of AWS nodes. 
m4.xlarge
m4.large
m4.2xlarge


@packet flow?
randomly selected (start, end) pairs from the network topology.
each flow associates with 1-4 VNFs. 
wikipedia trace
Arrival Process distribution


@packet routing?
how to route based on the VNF placement?
network latency model 
queuing delay



@VNF: resource requirement. execution time
# resource demand: number of VM
# random (0.2, 1)


how to model execution time?
Based on VNF throughput. 

@service chain?
Erd ̋os-Rényi model [48]to generate the graphs of VNF-FGs

'''


def main():
    env = simpy.Environment()


if __name__ == '__main__':
   main()

