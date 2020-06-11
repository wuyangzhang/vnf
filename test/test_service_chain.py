from core import ServiceChain


def main():
    service_chain = ServiceChain(10, vnf_graph=None)
    ServiceChain.random_gen()


if __name__ == '__main__':
    main()

