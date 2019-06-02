# -*- coding: utf-8 -*-
import Controle
import random
from lib_nrf24 import NRF24
from Controle import inicionrf24tx
from Controle import inicionrf24rx
from Controle import flag_tx
from Controle import flag_rx


while True:
    deteccao = random.randint(0,1)
    print("Detecção:", deteccao)
    if deteccao == 1:
        inicionrf24tx()
        flag_tx(deteccao)
    else:
        rx = inicionrf24rx()
        rele = flag_rx(rx)

