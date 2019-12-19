#!/usr/bin/python

"""
There are several classes built for Task Managers project.
These classes could be used as backend data collectors in further applications.
Classes:
    Day: interactive data structure, that stores tasks for any day.
"""
import pickle
import os
import warnings


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

    days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, date: str, source='') -> None:
        '''
        Here we init new Day. Every Day consists of
            Tasks to do during the current Day (dict)
                id: ['Description', (Achieved? bool True/False)]
            Tasks for tomorrow day -- plans (dict)
                id: ['Description', (Achieved? bool True/False)]
            Todays Insite (str)
            Date -- GNU Formated date oy current Day (list)
                ['YYY','MM','DD']
            Source -- root folder of current Day class (str) (got from args!)

        date: str 'YYYY-MM-DD' (as same as GNU format)
        <optional> source='': str: root folder for days. Must match '^/.*/$'
        '''
        self.source = source
        self.today_tasks = {0: ['Survive', True]}
        self.tomorrow_tasks = {0: ['Survive', True]}
        self.insite_of_day = ''
        self.dates = date.split('-')

        for i in self.dates[:-1]:
            source += (i + '/')
            try:
                os.mkdir(source)
            except FileExistsError:
                continue
        source += self.dates[-1]
        self.path = source

        self._file_conflict(err=True)  # Maybe it worth to set False..?

    @staticmethod
    def from_dump(dump_path: str):
        """
        This function gives to you ability to load existing Day dump from disk
        Function will read binary pickle dump and return Day class object

        dump_path: str: full or absolute path to pickle dump of Day object

        return: Day object
        """
        with open(dump_path, 'rb') as f:
            return pickle.load(f)

    def create_today_task(self, text: str) -> None:
        '''
        This method creating to the new one Task in block with parameter 'text'
        This block named: 'Today'

        text: str: task description
        '''
        key = list(self.today_tasks.keys())[-1] + 1
        self.today_tasks[key] = [text, False]

    def create_tomorrow_task(self, text: str) -> None:
        '''
        This method creates the new Task in this block with parameter 'text'
        This block named: 'Tomorrow'

        text: str: task description
        '''
        key = list(self.tomorrow_tasks.keys())[-1] + 1
        self.tomorrow_tasks[key] = [text, False]

    def import_previous_day(self) -> None:
        '''
        podsos - it is the best method which changed our life.
        It is perfect, truly. Seriously:
        This method integrates data from one previous object into the current
        '''
        year_old = int(self.dates[0])
        month_old = int(self.dates[1])
        day_old = int(self.dates[2])

        if day_old == 1:
            if month_old == 1:
                year_old -= 1
                month_old = 12
                day_old = 31
            else:
                month_old -= 1
                day_old = Day.days_in_months[month_old]
                if month_old == 2 and year_old % 4 == 0:
                    # Febraury, 1 day longer month
                    day_old += 1
        else:
            day_old -= 1

        old_source = self.source
        old_source += f'{str(year_old)}/{str(month_old)}/{str(day_old)}'

        with open(old_source, 'rb') as f:
            data_old = pickle.load(f)

        for i, value in data_old.tomorrow_tasks.items():
            if i != 0:
                self.create_today_task(value[0])

        del old_source

    def apply_task(self, id: int) -> None:
        '''
        This method changes the status of the Task

        id: int: id of task to change 'accepted' value (True <-> False)
        '''
        self.today_do[id][1] = not self.today_do[id][1]

    def dump(self) -> None:
        '''
        This method saves the data strusture of the object to the hard drive
        '''
        self._file_conflict()

        with open(self.path, 'wb') as f:
            pickle.dump(self, f)

    def _file_conflict(self, err=False) -> None:
        '''
        Private method that checks if self.path file already exists

        <optional> err=False: bool: will raise error if True or Warn if False.
        '''
        if os.path.exists(self.path):
            if err:
                raise FileExistsError(f"File {self.path} already exists!")
            else:
                warnings.warn(f"File {self.path} already exists!", Warning)

    def __str__(self) -> str:
        '''
        String representation of exemplar:

        YYY-MM-DD
        Today Tasks:
            ...
        Tomorrow Tasks:
            ...
        Todays insite:
            ...

        return: str
        '''
        date = '-'.join(self.dates)
        todays = [task[0] for task in self.today_tasks.values()]
        tomorrows = [task[0] for task in self.tomorrow_tasks.values()]
        insite = self.insite_of_day

        data = f"{date}\nDay Tasks:"
        for t in todays:
            data += f"\n\t{t}"
        data += "\nTomorrow Tasks:"
        for t in tomorrows:
            data += f"\n\t{t}"
        data += f"\nTodays insite:\n{insite}"

        return data
