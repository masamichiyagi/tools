# -*- coding: utf-8 -*-
import random
import os

#################################################
## Gloval Variables Definition
#################################################




###################################
## Main roop
###################################
def main():

    i=0
    for i in range(8):
        a = random.randint(1,10)
        b = random.randint(1,9)
        c = random.randint(1,9)
        print('({:02})  {} * {} ='.format(i+1, 10*a+b, 10*a+c))
        print(' {} * {} + {}*{} =    {} + {} ='.format(10*a+b+c, 10*a, b, c, (10*a+b+c)*10*a, b*c))
        print('          The answer is {}.'.format((10*a+b)*(10*a+c)))
        print('')
    # Q 9
    i+=1
    a = random.randint(1,9)
    b = random.randint(1,9)
    c = 10-b
    d = random.randint(1,9)
    print('({:02})  {} * {} ='.format(i+1, 100*d+10*a+b, 10*a+c))
    print('{} + {} * {} + {}*{} =  {} + {} + {} ='.format(100*d*(10*a+c), 10*a+b+c, 10*a, b, c, 100*d*(10*a+c), (10*a+b+c)*10*a, b*c))
    print('          The answer is {}.'.format((100*d+10*a+b)*(10*a+c)))
    print('')
    # Q 10
    i+=1
    a = random.randint(1,9)
    b = random.randint(1,9)
    c = 10-b
    print('({:02})  {} * {} ='.format(i+1,100*(10*a+b)+10*a+b, 10*a+c))
    print(' {} * {} + {}*{} ='.format(100*(10*a+b), 10*a+c, 10*a+b, 10*a+c))
    print('          The answer is {}.'.format((100*(10*a+b)+10*a+b)*(10*a+c)))
    print('')

    os.system('PAUSE')

if __name__ == '__main__':
    main()
