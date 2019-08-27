import sqlite3


class DBHelper:

    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS tasks (name text, percentage number, hours number, priority number, days number, percentageDone number, owner text)"
        tblstmt2 = "CREATE TABLE IF NOT EXISTS dailyHours (name text, hours number, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS taskIndex ON tasks (name ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON tasks (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(tblstmt2)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, task_name, task_percentage, task_hours, task_priority, task_days, task_percentageDone, owner):
        stmt = "INSERT INTO tasks (name, percentage, hours, priority, days, percentageDone, owner) VALUES (?,?,?,?,?,?,?)"
        args = (task_name, task_percentage, task_hours, task_priority, task_days, task_percentageDone, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_hours(self, day_name, day_hours, owner):
        stmt = "INSERT INTO dailyHours (name, hours, owner) VALUES (?,?,?)"
        args = (day_name, day_hours, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_hours(self, owner):
        stmt = "SELECT name, hours FROM dailyHours WHERE owner = (?)"
        args = (owner, )
        return [x for x in self.conn.execute(stmt, args)]

    def delete_item(self, task_name, owner):
        stmt = "DELETE FROM tasks WHERE name = (?) AND owner = (?)"
        args = (task_name, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT name FROM tasks WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_all_tasks(self, owner):
        stmt = "SELECT name, percentage, hours, priority, days, percentageDone FROM tasks WHERE owner = (?)"
        args = (owner, )
        return [x for x in self.conn.execute(stmt, args)]
