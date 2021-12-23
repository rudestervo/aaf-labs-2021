
# demo of db features


from database import Database
from parser import parse, parses


# demo of db features


# Create db:
db =Database()


# Create tables:

for command in parse('''

CREATE cats (cat_id INDEXED, cat_owner_id INDEXED, cat_name);
CREATE owners (owner_id INDEXED, age INDEXED, name);

'''):

    db.cmd(command)

# insert values

for command in parse('''

INSERT INTO owners("2", "25", "Kolya");
INSERT INTO owners("53", "535", "Vasya");
INSERT INTO owners("222", "15", "Dima");
INSERT INTO owners("2122", "14245", "11Dima");
INSERT INTO owners("2222", "1535", "11Dima");

insert INTO cats("22", "53", "Murzik");
INSERT INTO cats("99", "0", "Pushok");
INSERT INTO cats("666", "-5", "doggy");
INSERT INTO cats("142", "2", "CAT_UNIQUE");
INSERT INTO cats("111", "15", "iptshit");


'''):
    db.cmd(command)




# show tables

db.cmd(parses('''
select *  FROM owners;


'''))

db.cmd(parses('''
SELECT *  FROM cats WHERE name != NON-exist_NAME;


'''))

# delete some

db.cmd(parses('''

delete cats WHERE cat_name = Murzik
;

'''))



print()
print()

# full join
for command in parse('''
INSERT INTO cats("900", "111535", "Murzik-added-after");

'''):
    db.cmd(command)


db.cmd(parses('''

SELECT * FROM owners FULL_JOIN cats ON owner_id = cat_owner_id WHERE cat_name != Murzik;
;

'''))

