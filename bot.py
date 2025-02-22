import re
import datetime
from random import randint, choice, shuffle
from const import const
from helpers import helpers
from services import services

class Bot:
    """Класс Бот с заданными параметрами"""
    def __init__(self):
        self.name = const.NAME
        self.age = const.BORN_IN
        self.prev_answer = ''
        self.is_on = True
        self.phrases = helpers.file_to_list(const.MAIN_FILE)

    def check_key(self, question):
        """Обрабатывает ключевые вопросы"""
        return {
            'dt': str(datetime.datetime.fromtimestamp(const.BORN_IN)),
            'name': self.name,
        }.get(question)

    def get_shortest_element(self):
        """Возвращает первый элемент самой короткой строки"""
        shortest = min(self.phrases, key=len, default='')
        return services.get_first(shortest)

    def no_answer(self, question: str):
        """Обрабатывает ситуацию, когда нет ответа"""
        elm = self.get_shortest_element()
        rnd_val = randint(0, 100)
        if rnd_val > 100:
            return choice(const.DONT_KNOW_PHRASES)
        if rnd_val > 50 and elm:
            return elm

        question_words = question.split()
        for phrase in self.phrases:
            phrase_0 = services.get_first(phrase)
            line_list = re.findall(r'[^;\n]+', phrase_0.lower())
            if any(s.count(phrase_0) > 0 and len(s) > 1 for s in question_words) and len(line_list) > 1:
                return choice(line_list[1:])
        
        return services.get_first(choice(self.phrases))

    def save_new_phrases(self, question):
        """Сохраняет новые фразы"""
        prev_answer = self.prev_answer
        if prev_answer == question or any(prev_answer == services.get_first(s) for s in self.phrases):
            return
        self.phrases.append(prev_answer) if prev_answer else None
        self.phrases.append(question)

    def save_prev_answer(self, question):
        """Сохраняем предыдущ ответ, если вопрос есть в базе"""
        for i, s in enumerate(self.phrases):
            line_list = re.findall(r'[^;\n]+', s)
            if self.prev_answer == line_list[0] and self.prev_answer:
                self.phrases[i] = f"{s.rstrip()};{question}"
                break

    def find_answer(self, question):
        """Поиск ответа в базе"""
        min_letters = 6  # Найдет ответ только если более 6 букв совпало
        res = { "max": min_letters, "answers": [] } 
        for i, s in enumerate(self.phrases):
            line_list = re.findall(r'[^;\n]+', s)
            if len(line_list) > 1:
                db_question = line_list[0]
                db_answers = line_list[1:]
                number_of_letters = sum(len(word) if word in question.split() else 0 for word in db_question.split())
                if number_of_letters:
                    if number_of_letters >= res["max"]:
                        res["max"] = number_of_letters 
                        res["answers"] += db_answers
                    # print(db_question, db_answers, number_of_letters, res["max"])
        if res["answers"]:
            return choice(res["answers"])
        return None

    def get_answer(self, question):
        """Находит ответ на заданный вопрос"""
        self.question = helpers.str_clr(question).lower()
        if self.question == 'ex':
            self.is_on = False
            return 'Пока!'

        answer = self.check_key(self.question) or None
        if answer is None:
            self.save_new_phrases(self.question)
            self.save_prev_answer(self.question)
            answer = self.find_answer(self.question)
            answer = answer or self.no_answer(self.question)
            helpers.list_to_file(self.phrases, const.MAIN_FILE)
        
        self.prev_answer = helpers.str_clr(answer)
        return self.prev_answer
    
"""
Что надо сделать?
- можно расширять ответ, например: хм.., | могу предположить, что | ра
- попробовать подбирать ответы по числу вхождения: букв, слогов
"""
def additional():
    """Доп действия: убираю повторы в БД и короткие ответы"""
    from collections import Counter
    b = Bot()
    filtered_res = []
    questions = []
    for phrase in b.phrases:
        line_list = re.findall(r'[^;\n]+', phrase)
        question = line_list[0]
        if question:
            questions.append(question)
        answers = line_list[1:]
        filtered_answers = list(set(answers))
        if len(answers) != len(filtered_answers): # Повторы в ответах
            print(question, Counter(answers))
            pass
        if len(question) < 4:                   # Короткие вопросы
            print(question)
        if len(question) > 3:
            # Сохраняем только: длинные вопросы и не повторяющиеся ответы
            filtered_res.append(';'.join([question] + filtered_answers))


    counted_questions = Counter(questions)      # повторяющиеся вопросы
    for q in Counter(questions):
        if counted_questions[q] > 1:
            print(q, ':', counted_questions[q])
    
    filtered_res.sort()
    helpers.list_to_file(filtered_res, const.MAIN_FILE)
    # print(filtered_res)

def tests():
    phrase = 'кто ты такой'
    print(Bot().find_answer(phrase))

if __name__=='__main__':
    # additional()
    tests()

    