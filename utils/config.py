from enum import Enum,unique

class Token(Enum):
    tushare_token='3841b268c623d6c28f766ef1ffdd0b40737af355759ef44488f8e600'



if __name__=='__main__':
    print(Token.tushare_token.value)