import time

def returnHelloWorld():
    return 'Hello World !'

def repeat(msg):
    print(f'{msg=}')
    time.sleep(10)
    print(f'{type(msg)=}')
    return msg