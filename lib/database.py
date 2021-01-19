from sqlalchemy import Column, Integer, String, Table, Float
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData
from lib.dialog import Dialog

d = Dialog()
meta = MetaData()


def db(backend, dbname, username="", password="", host="localhost"):
    if backend == "SQLite":
        engine = create_engine(f'sqlite:///{dbname}')
        return engine
    else:
        engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{host}/{dbname}")
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine


students = Table(
    'students', meta,
    Column('name', String),
    Column('father_name', String),
    Column('mother_name', String),
    Column('phone', String),
    Column('addr', String),
    Column('class', String),
    Column('section', String),
    Column('roll_no', Integer),
    Column('english', Float),
    Column('math', Float),
    Column('science', Float),
    Column('computer', Float),
    Column('hindi', Float),
    Column('social', Float),
    Column('music', Float),
    Column('art', Float),
    Column('addmission_no', Integer, primary_key=True),
)


def create(engine):
    meta.create_all(engine)
    conn = engine.connect()
    return conn


def get_detail(conn, addmission_no):
    query = students.select(). \
        where(students.c.addmission_no == int(addmission_no))
    result = conn.execute(query)
    result = result.fetchone()
    return result


def update_student(connection, addmission_no, name="",
                   father_name="", mother_name="", phone="",
                   addr="", clss="", roll_no="", section=""):

    kwargs = {"name": name,
              "father_name": father_name,
              "mother_name": mother_name,
              "phone": phone,
              "addr": addr,
              "class": clss,
              "roll_no": int(roll_no) if roll_no else "",
              "section": section}

    kwargs_ = dict()
    for key in kwargs:
        if kwargs[key] != "":
            kwargs_[key] = kwargs[key]
    update = \
        students.update() \
        .where(students.c.addmission_no == int(addmission_no)) \
        .values(**kwargs_)
    result = connection.execute(update)
    result = connection.execute("commit")
    return result


def add_student(connection, addmission_no, name,
                father_name, mother_name, phone,
                addr, clss, roll_no, section):
    kwargs = {"addmission_no": int(addmission_no),
              "name": name,
              "father_name": father_name,
              "mother_name": mother_name,
              "phone": phone,
              "addr": addr,
              "class": clss,
              "roll_no": int(roll_no),
              "section": section}
    data = get_detail(connection, addmission_no)
    if not data:
        insert = students.insert().values(**kwargs)
        result = connection.execute(insert)
        connection.execute("commit")
        return result
    else:
        d.title = "Exists"
        d.text = "Data already exists. Do you want to update"
        d.open()
        if d.result == 1:
            update_student(**kwargs)


def delete(conn, addmission_no):
    delete = students.delete() \
        .where(students.c.addmission_no == int(addmission_no))
    result = conn.execute(delete)
    conn.execute("commit")
    return result


def add_marks(conn, addmission_no, marks):
    if len(marks) < 8:
        m_len = 8 - len(marks)
        marks = marks.split() + ["0"] * m_len
        marks = " ".join(marks)
        print(marks)
    new_marks = list(map(float, marks.split()))[:8]
    subjects = ('english', 'math', 'science', 'computer',
                'hindi', 'social', 'music', 'art')
    kwargs = dict(zip(subjects, new_marks))
    update = \
        students.update() \
        .where(students.c.addmission_no == int(addmission_no)) \
        .values(**kwargs)
    result = conn.execute(update)
    conn.execute("commit")
    return result


def find_marks(conn, addmission_no):
    data = get_detail(conn, addmission_no)
    marks = ""
    if data:
        for i in range(8, 16):
            marks += str(data[i]) + " "
    return marks
