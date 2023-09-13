import handlers_text
from FSM import get_state, set_state
from db import create_note, get_notes, get_note, delete_note
from utils import clear


async def start():
    print('Добро пожаловать в заметки, для взаимодействия введите число в начале строки')
    set_state('Menu')
    clear()
    await menu()
    while True:
        query = input()
        state = get_state()
        match query, state:
            case '1', 'Menu':
                clear()
                set_state('CreatingNote')
                await creating_note()
            case '2', 'Menu':
                clear()
                set_state('MyNotesView')
                await my_notes()
            case '0', 'MyNotesView':
                clear()
                set_state('Menu')
                await menu()
            case _, 'MyNotesView':
                clear()
                set_state('ViewNote')
                await viewing_note(query)
            case '0', 'ViewNote':
                clear()
                set_state('MyNotesView')
                await my_notes()
            case '3', 'Menu':
                clear()
                set_state('MyNotesFind')
                await get_query_to_find_note()
            case '0', 'MyNotesFind':
                clear()
                set_state('Menu')
                await menu()
            case _, 'MyNotesFind':
                clear()
                set_state('FindNotesView')
                await find_note(query)
            case '0', 'FindNotesView':
                clear()
                set_state('Menu')
                await menu()
            case '4', 'Menu':
                clear()
                set_state('MyNotesDelete')
                await my_notes()
            case '0', 'MyNoteDelete':
                clear()
                set_state('Menu')
                await menu()
            case _, 'MyNotesDelete':
                clear()
                await deleting_note(query)
            case _, 'Menu':
                clear()
                print('!!!Неверный ввод!!!')
                await menu()


async def menu():
    print(handlers_text.menu_text)


async def creating_note():
    print(handlers_text.get_title_text)
    title = input()
    print(handlers_text.get_content_text)
    content = input()
    create_note(title, content)
    clear()
    set_state('Menu')
    await menu()


async def my_notes():
    print(handlers_text.viewing_note_text)
    print(handlers_text.cancel_text)
    notes = get_notes()
    if not notes:
        print(handlers_text.no_notes_text)
    else:
        for note in notes:
            print(f'{note.rowid}) {note.title[:96] + "..." if len(note.title) > 96 else note.title}:\n'
                  f'{note.content[:97] + "..." if len(note.content) > 97 else note.content}')


async def viewing_note(query):
    if query.isdigit():
        note = get_note(int(query))
        if note is None:
            clear()
            print('!!!Несуществующая заметка!!!')
            await my_notes()
        else:
            clear()
            print(handlers_text.cancel_text)
            print(f'{note.title}:\n{note.content}')
    else:
        clear()
        set_state('MyNotesView')
        print('!!!Неверный ввод!!!')
        await my_notes()


async def get_query_to_find_note():
    print(handlers_text.key_word_text)
    print(handlers_text.cancel_text)


async def find_note(query):
    notes = get_notes()
    print(handlers_text.viewing_note_text)
    print(handlers_text.cancel_text)
    found = False
    for note in notes:
        if query in note.title or query in note.content:
            found = True
            print(f'{note.rowid}) {note.title[:96] + "..." if len(note.title) > 96 else note.title}:\n'
                  f'{note.content[:97] + "..." if len(note.content) > 97 else note.content}')
    if not found:
        print(handlers_text.not_found_text)


async def deleting_note(query):
    if query == '0':
        clear()
        set_state('Menu')
        await menu()
    elif query.isdigit():
        note = get_note(int(query))
        if note is None:
            clear()
            set_state('MyNotesDelete')
            print('!!!Несуществующая заметка!!!')
            await my_notes()
        else:
            delete_note(query)
            clear()
            print(handlers_text.deleting_success)
            set_state('Menu')
            await menu()
    else:
        clear()
        print('!!!Неверный ввод!!!')
        await my_notes()
