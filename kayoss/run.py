from satella.os import hang_until_sig
import logging
from kayoss.device import MyDevice


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    d = MyDevice()
    hang_until_sig()
    d.close()
