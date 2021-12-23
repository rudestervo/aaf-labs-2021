from database import Database
from parser import parse
from interface import message

# Create db:
db = Database()

while True:
    cmd = input("Enter db cmd:")
    if cmd == 'exit': # exit loop
        break

    for cmd in parse(cmd+";"):
        db.cmd(cmd)















        '''
        
 CREATE cats (cat_id INDEXED, cat_owner_id INDEXED, cat_name);
CREATE owners (owner_id INDEXED, age INDEXED, name);
INSERT INTO owners(2, 25, Kolya);
INSERT INTO owners(53, 535, Vasya);
INSERT INTO owners(222, 15, Dima);
INSERT INTO owners(2122, 14245, 11Dima);
INSERT INTO owners(2222, 1535, 11Dima);

insert INTO cats(22, 53, Murzik);
INSERT INTO cats(99, 0, Pushok);
INSERT INTO cats(666, -5, doggy);
INSERT INTO cats(142, 2, CAT_UNIQUE);
INSERT INTO cats(111, 15, iptshit);
select *  FROM owners;
SELECT *  FROM cats WHERE name != NON-exist_NAME;
delete cats WHERE cat_name = Murzik;

INSERT INTO cats(22, 535, Murzik1);
INSERT INTO cats(2, 222, Murzik2);
INSERT INTO cats(7, 0, Murzik3);
INSERT INTO cats(0, -9, Murzik4);
INSERT INTO cats(43, 1, Murzik5);
SELECT * FROM owners FULL_JOIN cats ON owner_id = cat_owner_id WHERE cat_name != Murzik;
;       
        
        
        
        '''

