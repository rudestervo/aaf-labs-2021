typedef struct stacks {
char * str;
struct stacks * next;
}stacks;


stacks * stacks_create();
void stacks_push(stacks ** root,char * str);
unsigned int stacks_count(stacks * root);
char * stacks_pop(stacks ** root);
void stacks_clear(stacks ** root);

void stacks_print(stacks * root);
