
from collections import OrderedDict
import datetime
import os

from peewee import * 

db = SqliteDatabase('reminder_app.db')


class reminder_app(Model):
    task = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    done = BooleanField(default=False)

    class Meta:
        database = db


def initialize():
    """DB creation/connection"""

    db.connect()
    db.create_tables([reminder_app], safe=True)


def view_entries(index, entries, single_entry):
    """"View reminder's"""

    os.system('cls' if os.name == 'nt' else 'clear') #clear screen

    index = index % len(entries)  # which entry is selected for modification
    if single_entry:  # to see only 1 entry in edit
        entries = [entries[index]]
        index = 0
    else:
        print('\nReminders:')
        print('=' * 40)
    prev_timestamp = None

    for ind, entry in enumerate(entries):
        timestamp = entry.timestamp.strftime('%d/%B/%Y')

        if timestamp != prev_timestamp:  # same timestamps get printed only once
            print('\n')
            print(timestamp)
            print('=' * len(timestamp))
            prev_timestamp = timestamp

        if ind == index:  # placing the selection tick
            tick = '> '
        else:
            tick = '  '

        print('{}{}'.format(tick, entry.task), end='')
        if entry.done:
            print('\t(Completed)', end='')
        print('')

    return entries  # so that we can modify the given entry if needed


def add_entry(index, entries):
    """Add a new reminder"""

    new_task = input('\nCreate Reminder: ')
    reminder_app.create(task=new_task)


def modify_entry(index, entries):
    """Modify selected entry"""
    entry = view_entries(index, entries, True)[0]
    print('\n\n')

    for key, value in sub_menu.items():
        print('{}) {}'.format(key, sub_menu[key].__doc__))
    print('q) Back to Main')
    next_action = input('Action: ')

    if next_action.lower().strip() in sub_menu:
        sub_menu[next_action](entry)
    else:
        return


def modify_task(entry):
    """Update reminder"""
    new_task = input('> ')
    entry.task = new_task
    entry.save()


def delete_entry(entry):
    """Delete entry"""
    if (input('Press "y" to confirm: ').lower().strip() == 'y'):
        entry.delete_instance()


def toggle_done(entry):
    """Toggle 'Completed'"""
    entry.done = not entry.done
    entry.save()


def menu_loop():
    choice = None
    index = 0  # shows which entry is selected
    entries = reminder_app.select().order_by(reminder_app.timestamp.asc())
    while choice != 'q':
        if len(entries) != 0:
            view_entries(index, entries, False)

            print('\n' + '=' * 40 + '\n')
            print('Task navigation \nup:p / down:n \n')
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        print('q) Quit')

        choice = input('\nAction: ')
        if choice in main_menu:
            try:
                main_menu[choice](index, entries)
            except ZeroDivisionError:
                continue
            entries = reminder_app.select().order_by(reminder_app.timestamp.asc())  # update entries after operations

        elif choice == 'n':
            index += 1
        elif choice == 'p':
            index -= 1


main_menu = OrderedDict([
    ('a', add_entry),
    ('m', modify_entry),
])

sub_menu = OrderedDict([
    ('m', modify_task),
    ('d', toggle_done),
    ('e', delete_entry)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
    db.close()
