all:
	gcc main.c dlist.c parse_str.c parse_comm.c dbase.c stacks.c -o mydb -g -lm -O0
zip:
	zip -r mydb.zip * *.* *.t
run:
	./mydb comm.t
prod:
	cp *.c *.h prod
