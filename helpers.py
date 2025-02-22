from const import const
import re

class helpers:

    @staticmethod
    def str_clr(val: str):
        """
        Очистка введеной строки:
            - убран перенос строки
            - убраны лишние пробелы
        """
        if not val: return ''
        return ' '.join(val.split())


    @staticmethod
    def file_to_list(fname: str):
        li_txt = []
        with open(fname, 'r') as f:
            li_txt = f.readlines()
        return [helpers.str_clr(s) for s in li_txt]


    @staticmethod
    def list_to_file(lst: list, fname: str):
        res_lst = [] 
        for s in lst:
            line = helpers.str_clr(s)
            if line.endswith(';'):
                line = line[:-1]
            res_lst.append(line + '\n') 
        with open(fname, 'w') as f:
            f.writelines(res_lst)


def test():
    test_str = helpers.str_clr("""Тестирую удаление
          переноса строки""")
    print(test_str, test_str[1:], test_str[:-1])
    # lst = helpers.file_to_list(const.MAIN_FILE)
    # print(lst)
    lst = ['я;я и ты;кто я;да ты;', 'ты бот а я человек;ты лучший', 'мы;это мы;мы люди;']
    helpers.list_to_file(lst, 'Chat_bot_2_new/tst.txt')

if __name__=='__main__':
    test()
    li_l = re.findall(r'[^;\n]+', 'hdjdhjhd;djdjdj,kkd;'.lower())
    l = 'hdjdhjhd;djdjdj,kkd;'.split(';')
    print(li_l, l)