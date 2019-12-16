#!/usr/bin/python

'''
There are several classes built for Task Managers project.
These classes could be used as backend data collectors in further applications.
Classes:
    Day: interactive data structure, that stores tasks for any day.
'''
import pickle
import os


class Day:
    """
    This class is needed to store data about a specific day. 
    Day is a class object. The __init__ method accepts today's as a 'date'
    and the global prefix as a 'source'.
    This class performs the following methods:
    1. Creating new Tasks in different parts of the data strusture
    2. The ability to integrate data from one previous object into the current
    3. The ability to change the status of the Task
    4. Saving the data strusture of the weaving object to the directory
    """

    days_per_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, date: str, source='') -> None:
        '''
        date: str 'YYYY-MM-DD' (as same as GNU format)
        source: str matches '^/.*/$'
        '''
        self.source = source
        self.today_do = {0: ['Survive', True]}
        self.tomorrow_do = {0: ['Survive', True]}
        self.insite_day = ''
        self.date = date.split('-')

        for i in self.date[:-1]:
            source += (i + '/')
            try:
                os.mkdir(source)
            except FileExistsError:
                pass
        source += self.date[-1]
        self.path = source

    @staticmethod
    def from_dump(dump_path: str):
        """
        This function gives to you ability to load existing Day dump from disk
        Function will read binary pickle dump and return Day class object

        dump_path: str: full or absolute path to pickle dump of Day object
        """
        with open(dump_path, 'rb') as f:
            return pickle.load(f)

    def input_today_do(self, text: str) -> None:
        '''
        This method creating to the new one Task in this block with parameter 'text'
        This block named: 'Today'
        The parameter 'text': str
        '''
        self.today_do[list(self.today_do.keys())[-1] + 1] = [text, False]

    def input_tomorrow_do(self, text: str) -> None:
        '''
        This method creating to the new one Task in this block with parameter 'text'
        This block named: 'Tomorrow'
        The parameter 'text': str
        '''
        self.tomorrow_do[list(self.tomorrow_do.keys())[-1] + 1] = [text, False]

    def podsos(self) -> None:
        '''
        podsos - it is the best method which changed ours life. It is perfect, truly. Seriously:
        This method integrates data from one previous object into the current
        '''
        year_old = int(self.date[0])
        month_old = int(self.date[1])
        day_old = int(self.date[2])

        if day_old == 1:
            if month_old == 1:
                year_old -= 1
                month_old = 12
                day_old = 31
            else:
                month_old -= 1
                day_old = Day.days_per_month[month_old]
        else:
            day_old -= 1

        old_source = self.source + f'{str(year_old)}/{str(month_old)}/{str(day_old)}'

        print(f"try {old_source}")

        with open(old_source, 'rb') as f:
            data_old = pickle.load(f)

        for i, value in data_old.tomorrow_do.items():
            if i != 0:
                self.input_today_do(value[0])

        del old_source

    def changest(self, id: int) -> None:
        '''
        This method changes the status ot the Task
        '''
        self.today_do[id][1] = not self.today_do[id][1]

    def dump(self) -> None:
        '''
        This method saves the data strusture of the weaving object to the hard drive
        '''
        with open(self.path, 'wb') as f:
            pickle.dump(self, f)

    def __str__(self) -> str:
        """
        String representation of exemplar:

        YYY-MM-DD
        Today Tasks:
            ...
        Tomorrow Tasks:
            ...
        Todays insite:
            ...
        """
        date = '-'.join(self.date)
        todays = [task[0] for task in self.today_do.values()]
        tomorrows = [task[0] for task in self.tomorrow_do.values()]
        insite = self.insite_day

        data = f"{date}\nDay Tasks:"
        for t in todays:
            data += f"\n\t{t}"
        data += "\nTomorrow Tasks:"
        for t in tomorrows:
            data += f"\n\t{t}"
        data += f"\nTodays insite:\n{insite}"

        return data
