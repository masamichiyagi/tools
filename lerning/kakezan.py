# -*- coding: utf-8 -*-
import random

#################################################
## Gloval Variables Definition
#################################################




###################################
## Main roop
###################################
def main():

    for i in range(10):
        a = random.randint(1,9)
        b = random.randint(1,9)
        print('({:02})  {} * {} ='.format(i+1, a, b))
        print('                        The answer is {}.'.format(a*b))
        print('')

if __name__ == '__main__':
    main()
