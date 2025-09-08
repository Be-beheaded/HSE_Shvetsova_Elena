# Реализуйте класс CourtCase.
#
# При вызове метода конструктора экземпляра (__init__) должны создаваться следующие атрибуты экземпляра:
# ●	case_number (строка с номером дела — обязательный параметр) передаётся в качестве аргумента при создании экземпляра
# ●	case_participants (список по умолчанию пустой)
# ●	listening_datetimes (список по умолчанию пустой)
# ●	is_finished (значение по умолчанию False)
# ●	verdict (строка по умолчанию пустая)
#
# У экземпляра должны быть следующие методы:
# ●	set_a_listening_datetime — добавляет в список listening_datetimes судебное заседание (структуру можете придумать сами)
# ●	add_participant — добавляет участника в список case_participants (можно просто ИНН)
# ●	remove_participant — убирает участника из списка case_participants
# ●	make_a_decision — вынести решение по делу, добавить verdict и сменить атрибут is_finished на True


class CourtCase:
    def __init__(self, case_number: int):
        self.case_number = case_number
        self.case_participants = []
        self.listening_datetimes = []
        self.is_finished = False
        self.verdict = ''

    def set_a_listening_datetime(self, datetime):
        self.listening_datetimes.append(datetime)

    def add_participant(self, inn):
        self.case_participants.append(inn)

    def remove_participant(self, inn):
        self.case_participants.remove(inn)

    def make_a_decision(self, verdict_final):
        self.verdict = verdict_final
        self.is_finished = True


court_case_1 = CourtCase(case_number = 234)
court_case_1.add_participant(234556778)
court_case_1.make_a_decision("fjgjgnfjfjfjf")
court_case_1.remove_participant(234556778)
print(court_case_1.case_number)








