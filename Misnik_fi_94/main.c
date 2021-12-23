#include <string.h>
#include <stdlib.h>
#include "parser.h"
#include <stdio.h>

int main(int argc, char * argv[]){
//dlist * tree = dlist_init();//дерево для стека команды
stacks * root =  NULL;
stacks * invroot =  NULL;
dbase * tables=dbase_init("test");//создаем базу данных
if (argc==2) {//если введен аргумент
FILE * datafile;
datafile = fopen(argv[1],"r");
if (!datafile) {puts("cant open file"); return -2;}//и это было имя сущевствующего файла
char command[0xff];



do{//читем команды из него
if(fgets(command,0xff,datafile)){
	//printf("------------Command acheive - %s !!!",command);
	parse_string(&root,command);//парсим команду в последовательность двусвязного списка
while (root) { 	stacks_push(&invroot,stacks_pop(&root));}
parse_comm(invroot,tables);//разбор команды
while (invroot) { printf("\n",stacks_pop(&invroot),invroot->next);}}
//puts("i home!!");

//stacks_clear(&root); //чистим стек команды
}while(!feof(datafile));//повторяем со следуюзей стркоой файла
fclose(datafile);//закрываем файл
 }//после чего и/или если файла не было
puts("Input commands...");
char cmnd[80];
char i,c;
do {//принимаем команды с стандартного ввода/вывода
printf("\n>>");
fflush(stdout);
fflush(stdin);
for (int i = 0;i<80;i++) cmnd[i]=0x20;
fgets(cmnd,80,stdin);
cmnd[strlen(cmnd)-1]=0;

parse_string(&root,cmnd);//парсим команду
while (root) { 	stacks_push(&invroot,stacks_pop(&root));}
parse_comm(invroot,tables);//разбор команды
while (invroot) { stacks_pop(&invroot);}

//printf("etc-%s %i",cmnd,strcmp(cmnd,"exit"));
}while (strcmp(cmnd,"exit")*strcmp(cmnd,"EXIT"));
puts ("Thats all, folks!");
return 0;//всё
}