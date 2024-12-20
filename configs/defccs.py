import random

def luhn_verification(num):
    num = [int(d) for d in str(num)]
    check_digit = num.pop()
    num.reverse()
    total = 0
    for i,digit in enumerate(num):
        if i % 2 == 0:
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        total += digit
    total = total * 9
    return (total % 10) == check_digit



def cc_gen(cc,mes='x',ano='x',cvv='x'):
    ccs = []
    while len(ccs) < 10:
        card = str(cc)
        digits = '0123456789'
        list_digits = list(digits)
        random.shuffle(list_digits)
        string_digits = ''.join(list_digits)
        card = card + string_digits
        if card[0] == '3':
            card = card[0:15]
        else:
            card = card[0:16]

        if mes == 'x':
            mes_gen = random.randint(1,12)
            if len(str(mes_gen)) == 1:
                mes_gen = '0' + str(mes_gen)
        else:
            mes_gen = mes

        if ano == 'x':
            ano_gen = random.randint(2023,2031)
        else:
            ano_gen = ano
            if len(str(ano_gen)) == 2:
                ano_gen = '20' + str(ano_gen)

        if cvv == 'x':
            if card[0] == '3':
                cvv_gen = random.randint(1000,9999)
            else:
                cvv_gen = random.randint(100,999)
        else:
            cvv_gen = cvv

        x = str(card) + '|' + str(mes_gen) + '|' + str(ano_gen) + '|' + str(cvv_gen)    
        a = luhn_verification(card)
        if a:
            ccs.append(x)
        else:
            continue

    return ccs