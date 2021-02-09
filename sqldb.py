import sqlite3

sqldbfile='mwdbSql1.sqlite'
table_name1 = 'imageshog'
field1 = 'name'
field2 = 'featuredescriptor'
field_type = 'TEXT'
conn = sqlite3.connect(sqldbfile)
c = conn.cursor()
c.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'\
        .format(tn=table_name1, fn=field1, ft=field_type))


c.execute("ALTER TABLE {tn} ADD COLUMN '{cn} {ft}'"\
         .format(tn=table_name1, cn=field2, ft=field_type))
conn.commit()
conn.close()