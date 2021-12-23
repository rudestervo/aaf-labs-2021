#include "stacks.h"
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

//---------------------------PUSH----------------------------
void stacks_push(stacks ** root,char * str){
stacks * p = (stacks*)malloc(sizeof(stacks));
//puts("push");
p->str=str;
p->next=(*root);
(*root)=p;
//printf("pushed %s ",(*root)->str);
return ;}
//---------------------------COUNT---------------------------
unsigned int stacks_count(stacks * root){
stacks * i = root;unsigned int count = 0;
while (i->next){count++;i=i->next;}return count;}
//---------------------------POP-----------------------------
char * stacks_pop(stacks ** root){
    stacks * prev = NULL;
    char * val;
    if (root == NULL) {
        exit(-1);
    }
    prev = (*root);
    val = prev->str;
    (*root) = (*root)->next;
    free(prev);
return val;}
//----------------------------PRINT-------------------
void stacks_print(stacks * root){
 if (root == NULL) {
        exit(-1);
    }
    stacks * p = root;
    while (p){
    printf("Stack - %s \n",p->str);
    p=p->next;
    }

}


//---------------------------CLEAR---------------------------
void stacks_clear(stacks ** root){



stacks * p;
puts("clear");
if(root==NULL) return;
//printf("%p %p  \n",*root,(*root)->next);

while ((*root)->next){
p=(*root)->next;
puts("clear");
free((*root)->str);
free(*root);
(*root)=p;
}
free((*root)->str);
(*root)->next=NULL;
}
