#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include "parser.h"
#include <ctype.h>

#define COMMA '.' //decimal divider


bool isSpacer(char * ch){//является ли символ пробельным
switch (ch[0]){
case 0x20:;
case '\t':;
case '\r':;
case '\n':;
return true;}
return false;}

bool isDivider(char * ch){//является ли символ разделительным
if ((*ch>0x20)&&(*ch<0x30)) return true;
if ((*ch>0x39)&&(*ch<0x41)) return true;
if ((*ch>0x5a)&&(*ch<61)) return true;
if (*ch>0x7a) return true;
return false;
}

bool isDigit(char * ch){//является ли символ цифрой
if ((*ch>0x2f)&&(*ch<0x3a)) return true;//0123456789
return false;}

bool isCharacter(char * ch){//является ли символ алфавитно/цифровым
if ((*ch>0x2f)&&(*ch<0x3a)) return true;//0123456789
if ((*ch>0x40)&&(*ch<0x5b)) return true;//ABC...Z
if ((*ch>0x60)&&(*ch<0x7b)) return true;///abs...z
return false;
}

bool isSymbol(char * ch){//является ли символ алфавит
if ((*ch>0x40)&&(*ch<0x5b)) return true;//ABC...Z
if ((*ch>0x60)&&(*ch<0x7b)) return true;///abs...z
return false;
}




void parse_string(stacks ** root, char * str){//функция пополняет список синтаксичесими элементами из строки
char len=0;//заводим счетчик символов для слов
for (char * ch=str;*ch!=0x00;ch++){//пробегаем по строке указателем на символ
	if (isCharacter(ch)) //если буква
		while (isCharacter(ch)) {//printf("%c",*ch);
				         ch++;len++;}//измерем длинну цифробуквенного слова
if (len) {//если чтото есть
	//printf(" len=%i\n",len);
	char * s = (char*)malloc(sizeof(char)*len+1);//выделем память под нйденное и символ окончания строки
	memcpy(s,ch-len,len);//копируем в выделенную память строку
	s[len]=0;//добавляем окончание строки
	//dlist_add(list,dnode_add(s,NULL));//заносим в список
	stacks_push(root,s);
	//printf("parsed - %s %i\n",s,strlen(s));
	}len=0;//обнуляем счетчик
if (isDivider(ch)) {char * c = (char*)malloc(sizeof(char)+1);//если нашли разделитель выделяем под него память
		    *c=*ch;//копируем значение
		    c[1]=0;
			stacks_push(root,c);
			//dlist_add(list,dnode_add(c,NULL));//заносим в список
			//printf("!%c\n",*c);
			}
}}      			

