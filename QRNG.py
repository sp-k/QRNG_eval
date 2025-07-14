from numpy.random import choice
from pickle import load


from numpy import exp

def prob(N, n):
    return [(exp(n/N)-1)*exp(-(-~i)*n/N)/(1-exp(-n)) for i in range(N)]


def size_conv(size):
    val = int(''.join(i for i in size if i.isdigit()))
    match size[-2]:
        case 'k':
            expo = 3
        case 'K':
            expo = 3
        case 'M':
            expo = 6
        case 'G':
            expo = 9
        case default:
            expo = 0
    if size[-1] == 'B':
        return 8*val*10**expo
    return val*10**expo


bit = 2**3
N = 2**bit

inp = [i/1000 for i in range(8, 1, -2)] + [i/100 for i in range(1, 5)] + [i/20 for i in range(1, 17)]


for mu_Td in inp:
    p = prob(N, mu_Td)

    with open("data", 'rb') as file:
        data = load(file)
    data[f"Act_{mu_Td}"] = p

    from pickle import dump
    with open("data", 'wb') as file:
        dump(data, file)


for mu_Td in inp:
    
    with open("data", 'rb') as file:
        p = load(file)[f"Act_{mu_Td}"]
        
    for length in range(3):#['1GB', '100MB', '1GB']:
        
        size = size_conv('1GB')//bit
        
        with open(f'Act1GB{length}_{mu_Td}.txt', 'a') as file:
            bit_list = choice(range(N), size = size, p = p)
            for bl in bit_list:
                b_r = bin(bl)[2:]
                while len(b_r) < bit:
                    b_r = '0' + b_r
                file.write(b_r)
            bit_list = None
            print(f'Created: Act1GB{length}_{mu_Td}.txt', end = '\t')

        with open(f'Act1GB{length}_{mu_Td}.txt', 'r') as file:
            data = file.read()
            print(f'\t{len(data) == size_conv("1GB")}')
        data = None

