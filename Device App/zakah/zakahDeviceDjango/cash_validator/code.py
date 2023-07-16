
import time

from nv9biller import Biller

accepted = False
money    = 0
port     = 'COM3'

def encode_money(value):
    money_value = value / 100
    return money_value


def biller_main():
    global accepted, money, port

    biller = Biller(port)
    print('-------------------')
    print('Cash Validator program')
    print('SN: {:08X}'.format(biller.serial))
    print('--------------------')

    print('Enable Validator...')
    biller.channels_set(biller.CH_ALL)
    biller.display_enable()
    biller.enable()

    money = 0

    print('insert some money (Ctrl+C to quit)')
    while True:
        try:
            events = biller.poll()

            if (len(events) == 0): continue
            #print(len(events))
            accepted = False
            for event in events:
                if (event.code == 0xEE):
                    money += encode_money(event.channel.value)
                    accepted = True

            if (accepted):
                print("Accepted")
                print("Money : " , money)
                # break
            #else:
            #    print("Rejected!")

            time.sleep(0.5)
        except KeyboardInterrupt:
            break

    print('Disabling biller...')
    biller.disable()
    biller.display_disable()
    biller.channels_set(None)

if __name__ == '__main__':
    biller_main()
    print("Money: ", money)
