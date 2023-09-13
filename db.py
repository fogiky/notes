import sqlite3


class Note(object):
    def __init__(self, rowid, title, content):
        self.rowid = rowid
        self.title = title
        self.content = content


def create_note(title, content) -> None:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO notes (title, content) VALUES (?, ?)''', (title, content))
        conn.commit()
    except:
        pass
    finally:
        conn.close()


def get_notes() -> list:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    try:
        notes = cursor.execute('''SELECT rowid, * from notes''').fetchall()
        conn.commit()
        return [Note(*note) for note in notes]
    except:
        pass
    finally:
        conn.close()


def get_note(rowid) -> Note:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    try:
        note = cursor.execute('''SELECT rowid, * from notes WHERE rowid=?''', (rowid,)).fetchone()
        conn.commit()
        return Note(*note)
    except:
        pass
    finally:
        conn.close()


def delete_note(rowid) -> None:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''DELETE FROM notes WHERE rowid=?''', (rowid,))
        conn.commit()
    except:
        pass
    finally:
        conn.close()