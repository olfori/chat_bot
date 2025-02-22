from random import randint, choice

class services:

    @staticmethod
    def get_first(val: str):
        """Поиск первого эл-та строки до разделителя ";", переведенный в нижний регистр"""
        return val.split(';')[0]
    
if __name__=='__main__':
    res = services.get_first('val')
    print(res)
    res = services.get_first('val;lkj')
    print(res)
    res = services.get_first('')
    print(res)
    res = services.get_first('v')
    print(res)

    lst = ['11', '222', '3333']
    print(choice(lst[1:]))

    shortest = min(lst, key=len, default='')
    print(shortest)