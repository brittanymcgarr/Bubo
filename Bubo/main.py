################################################################################
## Main                                                                       ##
## Entry point for running Bubo.                                              ##
################################################################################

from Brain.Brain import Brain


def main():
    bubo = Brain()
    bubo.listen()
    bubo.speak()


if __name__ == "__main__":
    main()
