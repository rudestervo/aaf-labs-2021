#include "Rect.h"
#include "R_Tree.h"
#include <vector>
#include <iostream>




int main()
{
	R_Tree tree = R_Tree();
	
	for (int i = 0; i < 5; i++) {
		tree.incert(Rect(i, i, i + 1, i + 1));
		tree.print_tree();

	}
	
	
	cout << tree.get_height() << endl;

	
	
	



}


