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
        a = 1
        b = random.randint(1,9)
        c = random.randint(1,9)
        print('({:02})  {} * {} ='.format(i+1, 10*a+b, 10*a+c))
        print(' {} * {} + {}*{} =    {} + {} ='.format(10*a+b+c, 10*a, b, c, (10*a+b+c)*10*a, b*c))
        print('          The answer is {}.'.format((10*a+b)*(10*a+c)))
        print('')

if __name__ == '__main__':
    main()
