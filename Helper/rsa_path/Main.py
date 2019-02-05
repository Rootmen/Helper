import re
from random import choice
from string import ascii_letters

import rsa as rsa
from rsa import PublicKey, PrivateKey

# Публичный ключ для RSA
Public_Rsa_key = PublicKey(8528460616836763783897561956462105596914954006532265911712311683380482486102630624564799783376409979607899614788126661049746076325444875429188307035856253, 65537)
Private_Key = PrivateKey(8528460616836763783897561956462105596914954006532265911712311683380482486102630624564799783376409979607899614788126661049746076325444875429188307035856253, 65537, 4717284852225959185899364037440702624291119256859402159079165944772304041129781901475469050294402307285587354096391573497657995816080121983368308792273473, 4902009478631967923449653186935907234780556621710806720657636519983995645904895561, 1739788683398639716463012009651288258585394195066471998081771727246292373)

# Функция создания пути и его шифрования
def Get_Path():
    Patch = ''
    Patch +=(''.join(choice(ascii_letters) for i in range(35)))
    Patch_as_bytes = str.encode(Patch)
    print(Patch)
    crypto = rsa.encrypt(Patch_as_bytes, Public_Rsa_key)
    return Patch, crypto
