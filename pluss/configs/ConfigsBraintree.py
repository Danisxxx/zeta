import uuid
import names
import base64
import random
import secrets
from dataclasses import dataclass


@dataclass
class BehaviorsBraintree:
    '''
Class Behaviors Braintree
    ~~~~~~~~~~~~~~~~~~~~~

    Esta classe es un clean o un codigo para las estructuras Braintree
    con el fin de mejorar el codigo, ejemplo:

    >>> from configs.ConfigsBraintree import BehaviorsBraintree 
    
    >>> SessionId = BehaviorsBraintree().SessionId()

    >>> print(SessionId)

    5abaa319-8ccb-4b60-915f-1d81387a8b45
    
    ... or RandomName:

    >>> username = BehaviorsBraintree().RandomName('username')
    >>> mail = BehaviorsBraintree().RandomName('email')
    >>> password = BehaviorsBraintree().RandomName('password')


Si quieres conocer mas acerca del clean puedes escribirme
al telegram https://t.me/RexAw4it.

:Developer: Rex Await ( ريكس ) 31/08/2024 '''


    @classmethod
    def __init__(self):
        pass
    
    
    @classmethod
    def correlation_id(self):
        self.id_corre = secrets.token_hex(16)
        return self.id_corre
    
    
    @classmethod
    def SessionId(self):
        self.id = str(uuid.uuid4())
        return self.id
    
    @classmethod
    def SaveResponseHhml(self, response:str):
        with open("ResponseHhml.html", "w", encoding="utf-8") as f:
            f.write(response)

    @classmethod         
    def Ccs(self, cards:str=None):
        if '|' in cards:   return cards.split('|')
        elif ':' in cards: return cards.split(':')
        elif ',' in cards: return cards.split(',')
        elif '-' in cards: return cards.split('-')

        return cards


    @classmethod
    def RandomName(self,dato:str=None):
        if dato == 'username': 
            self.username = "{}{}{}".format(
                    names.get_first_name(),
                    names.get_last_name(),
                    random.randint(1000000,9999999)
                    )
            return self.username
         
        elif dato == 'email': 
            self.email = "{}{}{}@gmail.com".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000,9999999)
            )
            return self.email
        
        elif dato == 'password': 
            self.password = "{}{}#{}".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000,9999999)
            )
            return self.password
        
        elif dato == 'numero':
            self.number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return self.number
        
        else:
            return 'valores incorrectos: >>>   BehaviorsBraintree().RandomName("username")'


    @classmethod
    def QueryText(
                    self, 
                    data:str = None, 
                    chainOne:str = None, 
                    chainTwo:str = None
                    ):
        
        self.uophs = data[ data.index(chainOne) + len (chainOne):data.index(chainTwo,  data.index(chainOne) + len (chainOne))]
        try:
            return self.uophs
        
        except: 
            return 'value not found' 
    

    @classmethod
    def DecodeBear(self, dato:str = None):
        self._tokenEncoding = base64.b64decode(dato).decode('utf-8') 
        self.bear_end = BehaviorsBraintree().QueryText(
            self._tokenEncoding, 
            '"authorizationFingerprint":"',  
            '","')

        return self.bear_end
    

    @classmethod
    def Response(self, response:str=None):   
        if   'avs_and_cvv' in response:                             return 'Approved! ✅', response
        elif 'Insufficient Funds' in response:                      return 'Approved! ✅', response
        elif 'avs: Gateway Rejected: avs' in response:              return 'Approved! ✅', response
        elif 'CVV.' in response:                                    return 'Approved! ✅', response
        elif 'Card Issuer Declined CVV' in response:                return 'Approved! ✅', response
        elif 'Invalid postal code and cvv' in response:             return 'Approved! ✅', response
        elif 'Nice! New payment method added' in response:          return 'Approved! ✅', response
        elif 'Payment method successfully added.' in response:      return 'Approved! ✅', response
        elif 'Invalid postal code or street address' in response:   return 'Approved! ✅', response 
        elif 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number' in response:                return 'Approved! ✅', response
        else:                                                       return 'Declined! ❌', response