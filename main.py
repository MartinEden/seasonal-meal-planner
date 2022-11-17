import django
import calendar


def create_tables(db):
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE months(id INTEGER PRIMARY KEY, name TEXT)
''')
    cursor.execute('''
    CREATE TABLE recipes(id INTEGER PRIMARY KEY, name TEXT)
''')
    cursor.execute('''
        CREATE TABLE ingredients(id INTEGER PRIMARY KEY, name TEXT)
    ''')
    cursor.execute('''
        CREATE TABLE recipes_ingredients(ingredient_id INTEGER, recipe_id 
            INTEGER
    ''')
    cursor.execute('''
        CREATE TABLE months_ingredients(month_id INTEGER, ingredient_id 
        INTEGER)
    ''')
    cursor.execute('''
        CREATE TABLE tags(id INTEGER PRIMARY KEY, name TEXT)
    ''')
    cursor.execute('''
        CREATE TABLE tags_ingredients(tag_id INTEGER, ingredient_id 
        INTEGER)
    ''')
    db.commit()


db = sqlite3.connect('data/mealplannerdb')

# Get a cursor object
cursor = db.cursor()


create_tables(db)

for month in calendar.month_name:
    cursor.execute('''INSERT INTO months(name)
                      VALUES(?)''', month)
db.commit()

db.close()