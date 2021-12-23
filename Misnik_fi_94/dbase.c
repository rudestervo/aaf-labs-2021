#include "dbase.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

//***********************************************************************
//-------------------------BASE WORKING
//***********************************************************************
//---------------------------------------СОЗДАНИЕ БАЗЫ
dbase * dbase_init(char * name){//создать базу данных
dbase * p = (dbase *)malloc(sizeof(dbase));
if (!p) return NULL;
p->name=name;//имя базы
p->count=0;//количество таблиц
p->head=NULL;//ссылка на последнюю таблицу
p->tail=NULL;//ссылка на первую таблицу
return p;
}
//----------------------------------------ДОБАВЛЕНИЕ ТАБЛИЦЫ В БАЗУ в конец
unsigned int dbase_add ( dbase * base , dtable * table){//добавление таблицы в конец
//puts("dbase add");
if (dbase_is_empty(base)){//puts("empty");
base->head=table;//если база еще пустая
base->tail=table;//таблица одновременно и первая и последняя
//puts("-----------add in empty---------");
}  else
{//если база не пустая
table->prev=base->head;//передаем в предыдущее добаляемой таблицы верхнюю таблицу базы
table->prev->next=table;//меняем в бывшей верхней таблицы следующее на текущюю
base->head=table;//устанавливаем добавляему таблицу в базе как последнюю
//puts("add in not empty");
}
base->count++;//приращиваем значение счетчика таблиц в базе
table->base=base;//устанавливаем принадлежность в таблице
return base->count;//успех - возвращаем количество таблиц в базе
}

//----------------------------------------ОЧИСТКА БАЗЫ
void dbase_clear(dbase * base){
if (!base->tail) return;//если в хвосте чтото есть
dtable * p = base->tail;//устанавливаем указательно него
while(p) {//по указатель указывает на таблицу
	dbase_remove(p);//передаем таблице удалиться
	if (p->next) {p=p->next;} //если есть следующая то загружаем ее указатель в счетчик
		else return;}//а если нет, то выходим
}
//------------------------------------------ДОБАВЛЕНИЕ ТАБЛИЦЫ В БАЗУ в начало
unsigned int dbase_ins(dbase * base, dtable * table){ //вставка таблицы в начало
if (dbase_is_empty(base)){//puts("empty");//если пусто
base->head=table;//то все просто
base->tail=table;//наша таблица и альфа и омега
} else {base->tail->prev=table;//сообщаем бывшему хвосту кто теперь хвост
table->next=base->tail;//записываем в таблицу, что хвост теперь следующий
base->tail=table;//а в базу записываемся как на хвост
}base->count++;//приращиваем счетчик таблиц
table->base=base;//устанавливаем принадлежность к таблице
return base->count;//возвращаем результат - количество таблиц в базе
}
//-------------------------------------------ПУСТАЯ ЛИ БАЗА?
bool dbase_is_empty(dbase * base){//
if (!base->head&&!base->tail) {//если указатели на первый и последний элементы
if (base->count) puts("Base is empty but count!=0");//просто указываем на странность
return true;}//указывают на пустоту то база пустая
return false;}
//------------------------------------------НЕ ОДНА ЛИ ТАБЛИЦА В БАЗЕ?
bool dbase_is_trivial(dbase * base){//в базе однав таблица
if (base->head==base->tail) return true;//потому что альфа он же и омега
return false;}
//------------------------------------------УДАЛЕНИЕ ТАБЛИЦЫ ИЗ БАЗЫ

dtable * dbase_remove(dtable * table){//
if (!table) return NULL;//если передали пустой указатель то выходим
//puts("dbase_remove");
//printf("base->count=%li >>",base->count);
if (!table->base->count) table->base->count--;//если не ноль то вычитаем счетчик таблиц
//if (!base) puts("base NULL");
//printf("base->count=%li \n",base->count);
if (!table->base->count){//если в таблице ноль
table->tail=NULL;//в хвосте никого
table->head=NULL;//и нигде никого
table->base=NULL;//и база не моя
return table;//возвращаем ссылку на удаляемую таблицу
}
if (table==table->base->head) {//если таблица в голове
table->prev->next=NULL;//у предыдущей таблицы не будет следующей
table->base->head=table->prev;//назначаем предыдущую головной
table->base=NULL;//уходим из базы
table->next=NULL;//соседей нет
table->prev=NULL;
return table;//уходим
}
if (table==table->base->tail) {//если таблица в хвосте
table->next->prev=NULL;//следующую таблицу задаем как  последнюю
table->base->tail=table->next;//назначаем следующую последней
table->base=NULL;//уходим из базы
table->next=NULL;//соседей нет
table->prev=NULL;
return table;//выходим
}
//если были гдето в серердине
table->next->prev=table->prev;//указываем следующей предыдущего
table->prev->next=table->next;//и предыдущей следующего
table->next=NULL;//соседей нет
table->prev=NULL;
table->base=NULL;//уходим из базы
return table;
}
dtable * dbase_find(dbase * base,char * name){//
for(dtable * p = base->tail;p!=NULL;p=p->next)
	if (!strcmp(p->name,name)) return p;
return NULL;}
//*********************************************************************
//-------------------------TABLE WORKING
//*********************************************************************
//--------------------------------------СОЗДАЕМ ТАБЛИЦУ
dtable * dtable_create(char * name ){
dtable * p = (dtable*)malloc(sizeof(dtable));//выделяем память
p->name=name;//задаем указатель на имя
p->next=NULL;//соседей пока нет
p->prev=NULL;
printf("Memory for table %s on adress %p allocated\n",name,p);//сообщаем про результат
return p;}//возвращаем указатель
//--------------------------------------ДОБАВЛЯЕМ КОЛОНКУ К ТАБЛИЦЕ
unsigned int dtable_add(dtable * table , dcol * col){//добавление в конец
//puts("dbase add");
if (dtable_is_empty(table)){//puts("empty");//если таблица пустая
table->head=col;//все тривиально
table->tail=col;//
//puts("-----------add in empty---------");
}  else
{//текущая значит добавляемая
col->prev=table->head;//головная колонка таблицы теперь предыдущая для текущей
col->prev->next=col;//задаем в предыдущей текущую как следующую
table->head=col;//записываем в таблицу новую колонку как омегу
//puts("add in not empty");
}
table->count++;//увеличиваем счетчик колонок
col->table=table;//прописываемся
return table->count;//возвращаем количество колонок
}
//--------------------------------------УДАЛЕНИЕ КОЛОНОК ИЗ ТАБЛИЦЫ
dcol * dtable_remove(dcol * col){//
if (!col) return NULL;//если передали пустой указатель то выходим
//puts("dtable_remove");
//printf("table->count=%li >>",table->count);
if (!col->table->count) col->table->count--;//если не ноль то вычитаем счетчик колонок
//if (!table) puts("table NULL");
//printf("table->count=%li \n",table->count);
if (!col->table->count){//если в таблице ноль
col->table->tail=NULL;//в хвосте никого
col->table->head=NULL;//и нигде никого
col->table=NULL;//и  таблица не моя
return col;//возвращаем ссылку на удаляемую колонку
}
if (col==col->table->head) {//если колонка в голове
col->prev->next=NULL;//у предыдущей колонки не будет следующей
col->table->head=col->prev;//назначаем предыдущую головной
col->table=NULL;//уходим из таблицы
col->next=NULL;//соседей нет
col->prev=NULL;
return col;//уходим
}
if (col==col->table->tail) {//если колонка в хвосте
col->next->prev=NULL;//следующую колонку задаем как  последнюю
col->table->tail=col->next;//назначаем следующую последней
col->table=NULL;//уходим из таблицы
col->next=NULL;//соседей нет
col->prev=NULL;
return col;//выходим
}
//если были гдето в серердине
col->next->prev=col->prev;//указываем следующей предыдущего
col->prev->next=col->next;//и предыдущей следующего
col->next=NULL;//соседей нет
col->prev=NULL;
col->table=NULL;//уходим из таблицы
return col;
}
//------------------------------------ПОИСК СТОЛБЦА В ТАБЛИЦЕ
//реализован далее
//-------------------------------------В ТАБЛИЦЕ ЧТОТО ЕСТЬ?
bool dtable_is_empty(dtable * table){
if (!table->head&&!table->tail) return true;
return false;}
//------------------------------------ВЫВОД ТАБЛИЦЫ 
unsigned int dtable_print_all (dtable * table){//
puts("PRINT WHOLE TABLE");
dcell * c;
unsigned int ind = 0;
unsigned int max_row=table->tail->count;//количество строк для вывода
printf("Rows to print=%i\n",max_row);
char * s;//

//выводим заговолок - названия столбцов
printf("+--+");//рисуем таблицу
for (dcol * prn_col = table->head;prn_col!=NULL;prn_col=prn_col->prev) printf("--------------------+");
printf("\n|No|");//печатаем псевдографику
for (dcol * prn_col = table->head;prn_col!=NULL;prn_col=prn_col->prev) {
			
		printf("%20s|", prn_col->name);}


printf("\n+--+");
for (dcol * prn_col = table->head;prn_col!=NULL;prn_col=prn_col->prev) printf("--------------------+");
//печатаем ячейки
  for(unsigned int  i = 1;i!=max_row+1;i++)  {//побегаем по строкам
  	printf("\n|%2i|",ind);//псевдографика
  	ind++;
	for (dcol * prn_col = table->head;prn_col!=NULL;prn_col=prn_col->prev){//пробегаем по колонкам
           c = dcol_find_cell_index(prn_col,i);//ищем строку в колонке по текущему индексу строки
           
           if (c) {printf ("%20s|",c->string);} else //печатаем если ячейка в колонке с таким индексом есть
           		printf("%20s|","-NaN-");//если нет то данные не укaзны при добавлении колонки
	}
	}
printf("\n+--+");
for (dcol * prn_col = table->head;prn_col!=NULL;prn_col=prn_col->prev) printf("--------------------+");
printf("\nPrinting succesfull...\n");
return ind;}


//-------------------------------------ВЫВОД ТАБЛИЦЫ НА ПЕЧАТЬ
unsigned int dtable_print_todo (dptodo * todo){
// функция печати таблицы согласно задания todo 
puts("PRINT TABLE");
dcell * c;
unsigned int ind = 0;
unsigned int max_row=todo->col->count;//количество строк для вывода
printf("Rows to print=%i\n",max_row);
char * s;//

//выводим заговолок - названия столбцов
printf("+--+");//рисуем таблицу
for (dptodo * prn_col = todo;prn_col!=NULL;prn_col=prn_col->next) printf("--------------------+");
printf("\n|No|");//печатаем псевдографику
for (dptodo * prn_col = todo;prn_col!=NULL;prn_col=prn_col->next) {
			
		printf("%20s|", prn_col->col->name);}


printf("\n+--+");
for (dptodo * prn_col = todo;prn_col!=NULL;prn_col=prn_col->next) printf("--------------------+");
//печатаем ячейки  
  for(unsigned int  i = 1;i!=max_row+1;i++)  {//побегаем по строкам
  	printf("\n|%2i|",ind);//псевдографика
  	ind++;
	for (dptodo * prn_col = todo;prn_col!=NULL;prn_col=prn_col->next){//пробегаем по колонкам
           c = dcol_find_cell_index(prn_col->col,i);//ищем строку в колонке по текущему индексу строки
           
           if (c) {printf ("%20s|",c->string);} else //печатаем если ячейка в колонке с таким индексом есть
           		printf("%20s|","-NaN-");//если нет то данные не укaзны при добавлении колонки
	}
	}
printf("\n+--+");
for (dptodo * prn_col = todo;prn_col!=NULL;prn_col=prn_col->next) printf("--------------------+");
printf("\nPrinting succesfull...\n");
return ind;}
//----------------------------------------СОЗДАНИЕ ЗАДАНИЯ
dptodo * dtable_create_todo(dtable * table,char * colname){//создать задание
dptodo * todo = (dptodo*)malloc(sizeof(dptodo));//выделяем память
todo->col=dtable_find(table,colname);//ищем первую колонку
todo->next=NULL;//следующей пока нет
printf("Todo created. Col %s addet in todo\n", todo->col->name);
return todo;} //возвращаем результат
//----------------------------------------ДОБАВЛЕНИЕ К ЗАДАНИЮ
dptodo * dtable_todo_add(dptodo * todo,char * colname){//добавить к заданию
dcol * col = dtable_find(todo->col->table,colname);//ищем колонку по названию
if (col) { dptodo * new_todo = (dptodo *)malloc(sizeof(dptodo));//если нашли
		puts("Adding");
            new_todo->col=col;
		if (todo->col->count>new_todo->col->count) new_todo->col->count=todo->col->count;
            new_todo->next=todo;
            printf("Column %s found with len=%i todo %p added\n",col->name,col->count,(void*)new_todo);
	    return new_todo;}else 
	{printf("Column %s - not found\n",colname);}
return todo;}
//----------------------------------------ПОИСК КОЛОНКИ ПО НАЗВАНИЮ
dcol * dtable_find(dtable * table,char * colname){//поиск столбца по имени.
for (dcol * col = table->tail;col!=NULL;col=col->next)//пробегаем все столбцы
  if (!strcmp(col->name,colname)){ printf("Found col %s \n",col->name);
  	return col;}//если совпало возвращаем указатель
return NULL;} //если не нашли ничего то возвращаем NULL
//-----------------------------------------------------------------------------
//****************************************************************************
//--------------------------COLUMN WORKING
//****************************************************************************
//--------------------------------------СОЗДАНИЕ КОЛОНКИ
dcol * dcol_create(char * name, dindex * index){//создаем колонку
dcol * p = (dcol *)malloc(sizeof(dcol));//выделяем память
p->tail=NULL;//ячеек еще нет
p->head=NULL;//
p->count=0;//от слова совсем
p->name=name;//задаем имя
p->indexed=index;//индексируемая (или нет)
p->table=NULL;//таблица может и есть но не про её честь
printf("Column by adress %p sucessfully created\n",p);
return p;}//возвращаем указатель
//----------------------------------------ПУСТАЯ ЛИ КОЛОНКА?
bool dcol_is_empty(dcol * col){
if (!col->head&&!col->tail) return true;
return false;}
//----------------------------------------ДОБАВЛЯЕМ ЯЧЕЙКУ
int dcol_add(dcol * col,dcell * cell){//в колонку
if (dcol_is_empty(col)){//puts("empty");//если колонка пустая
col->head=cell;//все тривиально
col->tail=cell;//
//puts("-----------add in empty---------");
}  else 
{//текущая значит добавляемая
cell->prev=col->head;//головная ячейка таблицы теперь предыдущая для текущей
cell->prev->next=cell;//задаем в предыдущей текущую как следующую
col->head=cell;//записываем в колонку новую ячейку как последнюю
//puts("add in not empty");
}

col->count++;//увеличиваем счетчик ячеек
cell->index=col->count;
cell->col=col;//прописываемся
return col->count;//возвращаем количество ячеек
}
//---------------------------------------УДАЛЕНИЕ ЯЧЕЙКИ
dcell * dcol_remove(dcell * cell){//
if (!cell) return NULL;//если передали пустой указатель то выходим
if (!cell->col->count) cell->col->count--;//если не ноль то вычитаем счетчик колонок
if (!cell->col->count){//если в колонке ноль 
cell->col->tail=NULL;//в хвосте никого
cell->col->head=NULL;//и нигде никого
cell->col=NULL;//и  колонка не моя
return cell;//возвращаем ссылку на удаляемую ячейку
}
if (cell==cell->col->head) {//если ячейка в голове
cell->prev->next=NULL;//у предыдущей ячейки не будет следующей
cell->col->head=cell->prev;//назначаем предыдущую головной
cell->col=NULL;//уходим из колонки
cell->next=NULL;//соседей нет
cell->prev=NULL;
return cell;//уходим
}
if (cell==cell->col->tail) {//если ячейка в хвосте
cell->next->prev=NULL;//следующую ячейку задаем как  последнюю
cell->col->tail=cell->next;//назначаем следующую последней
cell->col=NULL;//уходим из колонки
cell->next=NULL;//соседей нет
cell->prev=NULL;
return cell;//выходим
}
//если были гдето в середине
cell->next->prev=cell->prev;//указываем следующей предыдущего
cell->prev->next=cell->next;//и предыдущей следующего
cell->next=NULL;//соседей нет
cell->prev=NULL;
cell->col=NULL;//уходим из колонки
return cell;
}
//--------------------------------------ПОИСК ЯЧЕЙКИ В КОЛОНКЕ ПО ИНДЕКСУ
dcell * dcol_find_cell_index(dcol*col,unsigned int index){//
for (dcell * i = col->tail;i!=NULL;i=i->next)
     if(i->index==index) {return i;}//printf("cell %i proseed ",i->index);
  //  printf("fail found ");
return NULL;
}
//-----------------------------------------------------------------------------
//****************************************************************************
//--------------------------CELL WORKING
//****************************************************************************
//--------------------------------------СОЗДАНИЕ ЯЧЕЙКИ
dcell * create_cell(char * str){
dcell * p = (dcell*)malloc(sizeof(dcell));//выделяем память
p->index=0;//индекса нет
p->col=NULL;//колонки нет
p->prev=NULL;//вокруг никого
p->next=NULL;//сирота
p->string=str;
printf("Cell %s by adress %p sucessfully created\n",str,p);//радуемся
return p;}//возвращаем сыслку на ячейку

