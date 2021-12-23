#include <stdbool.h>


typedef struct dnode {
struct dnode * prev;
struct dlist * list;
char * str;
int * num;
struct dnode * next; } dnode;   
	        

typedef struct dlist {
struct dnode * head;
struct dnode * tail;
long count;          } dlist;

	             
dlist * dlist_init();

dnode * dlist_remove(dnode * node);

void dlist_clear(dlist * list);

int dlist_add(dlist * list,dnode * node);//добавление узла в конец

int dlist_ins(dlist * list, dnode * node);//вставка узла в начало

bool dlist_is_empty(dlist * list);

bool dlist_is_trivial(dlist * list);


unsigned long dlist_list(dlist * list);//вывод узлов

dnode * dlist_remove(dnode * node);//удаление узла

dnode * dnode_add(char * str,int * num);

int dnode_print(dnode * node);

dlist * dlist_sort(dlist * list);


dnode * dlist_max(dlist * list);

dnode * dlist_min(dlist * list);
