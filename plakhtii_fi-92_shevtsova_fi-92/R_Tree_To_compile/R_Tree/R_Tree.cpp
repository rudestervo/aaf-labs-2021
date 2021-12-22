#include "R_Tree.h"





R_Tree::R_Tree()
{
	root = new Node(true, true);
	root->rect = Rect(0, 0, 0, 0);

}

void R_Tree::incert(Rect rect)
{
	this->_insert(rect);
}

vector<Rect> R_Tree::search(Rect rect)
{
	vector<Rect> res;
	_search(rect, root, res);
	return res;
}

void R_Tree::print_tree()
{
	root->_print_tree("", true);
}

int R_Tree::get_height()
{
	int res = 0;
	root->height(res);
	return(res);
}

void R_Tree::test()
{
	cout << root->rect << endl;
	cout << root->children[0]->rect << endl;
	cout << root->children[0]->data[0] << endl;




}



void R_Tree::_search(Rect rect, Node* T, vector<Rect>& result)
{
	if (!T->is_leaf) {
		for (int i = 0; i < T->children.size(); i++) {
			if (Rect::is_overlap(T->children[i]->rect, rect))
				R_Tree::_search(rect, T->children[i], result);

		}
	}
	else {
		for (int i = 0; i < T->data.size(); i++)
			if (Rect::is_overlap(T->data[i], rect))
				result.push_back(T->data[i]);
	}
}


void R_Tree::_insert(Rect rect)
{
	Node* leaf_to_insert = _choose_leaf(rect);
	if (!leaf_to_insert->is_full()) {
		leaf_to_insert->insert(rect);
		R_Tree::_adjust_tree(leaf_to_insert, nullptr);
	}
	else {
		leaf_to_insert->insert(rect);
		Node** splited_nodes = R_Tree::_split_node(leaf_to_insert);
		Node* L1 = splited_nodes[0];
		Node* L2 = splited_nodes[1];
		/*for (int i = 0; i < L1->data.size(); i++) {
			cout << "L1: " << L1->data[i] << endl;
		}
		for (int i = 0; i < L2->data.size(); i++) {
			cout << "L2: " << L2->data[i] << endl;
		}*/
		R_Tree::_adjust_tree(L1, L2);

	}


}


R_Tree::Node* R_Tree::_choose_leaf(Rect rect)
{
	Node* N = R_Tree::root;
	while (true) {
		if (N->is_leaf)
			return N;
		else
			N = R_Tree::_choose_subtree(N, rect);
	}
	return N;
}

void R_Tree::_adjust_tree(Node* L1, Node* L2)
{

	Node* N = L1;
	Node* NN = L2;



	while (true) {


		N->rect = R_Tree::adjust_rect(N);
		if (N->parent == nullptr)
			break;
		if (NN != nullptr) {
			NN->rect = R_Tree::adjust_rect(NN);
			if ((N->parent->children.size() + 2 <= Max_entries)) {
				N->parent->children.push_back(N);
				N->parent->children.push_back(NN);
				NN = nullptr;
				N = N->parent;
			}
			else
			{
				N->parent->children.push_back(N);
				N->parent->children.push_back(NN);
				Node** splited_nodes = R_Tree::_split_node(N->parent);
				N = splited_nodes[0];
				NN = splited_nodes[1];

			}
		}
		else
			N = N->parent;

	}
	if (N->parent == nullptr && NN != nullptr && NN->parent == nullptr) {
		this->root = new Node(true, false);
		this->root->children.push_back(N);
		this->root->children.push_back(NN);
		N->parent = this->root;
		NN->parent = this->root;
		this->root->rect = R_Tree::adjust_rect(this->root);

	}









}

R_Tree::Node* R_Tree::_choose_subtree(Node* N, Rect rect)
{
	Node* subtree = N->children[0];
	double min_area_to_increase = Rect::area_to_increase(N->children[0]->rect, rect);

	for (int i = 1; i < N->children.size(); i++) {
		if (Rect::area_to_increase(N->children[i]->rect, rect) < min_area_to_increase) {
			min_area_to_increase = Rect::area_to_increase(N->children[i]->rect, rect);
			subtree = N->children[i];
		}
	}
	return subtree;
}

void R_Tree::_delete(Rect rect)
{
	Node* leaf = nullptr;
	R_Tree::_find_leaf(this->root, rect, leaf);
//	if (leaf == nullptr) {
//		throw exception("The elemrnt not exist");
//	}
	leaf->data.erase(remove(leaf->data.begin(), leaf->data.end(), rect));
	R_Tree::_condense_tree(leaf);
	/*if the root has only one child => make the child the new root*/

}

R_Tree::Node** R_Tree::_split_node(Node* N)
{

	Node** result = new Node * [2];

	if (!N->is_leaf) {
		Node** seeds = R_Tree::_pick_seeds(N->children);
		vector<Node*> G1;
		vector<Node*> G2;
		N->children.erase(remove(N->children.begin(), N->children.end(), seeds[0]));
		N->children.erase(remove(N->children.begin(), N->children.end(), seeds[1]));
		G1.push_back(seeds[0]);
		G2.push_back(seeds[1]);
		while (true) {
			if (N->children.size() <= 0)
				break;
			if ((int)min(G1.size(), G2.size()) + N->children.size() - (int)max(G1.size(), G2.size()) <= Min_entries) {
				if (G1.size() < G2.size())
					G1.insert(G1.end(), N->children.begin(), N->children.end());
				else
					G2.insert(G2.end(), N->children.begin(), N->children.end());
				N->children.clear();
			}
			else {
				R_Tree::_pick_next(N->children, G1, G2);
			}
		}

		if (N->parent != nullptr)
			N->parent->children.erase(remove(N->parent->children.begin(), N->parent->children.end(), N));
		result[0] = new R_Tree::Node(false, false);
		result[0]->children = G1;
		for (int i = 0; i < G1.size(); i++)
			G1[i]->parent = result[0];
		result[0]->rect = R_Tree::adjust_rect(result[0]);
		result[0]->parent = N->parent;
		result[1] = new R_Tree::Node(false, false);
		result[1]->children = G2;
		for (int i = 0; i < G2.size(); i++)
			G2[i]->parent = result[1];
		result[1]->rect = R_Tree::adjust_rect(result[1]);
		result[1]->parent = N->parent;
		delete N;


	}
	else {


		/*for (int i = 0; i < N->data.size(); i++)
			cout << "splited node: " << N->data[i] << endl;*/

		Rect* seeds = R_Tree::_pick_seeds_leaf(N->data);
		vector<Rect> G1;
		vector<Rect> G2;

		N->data.erase(remove(N->data.begin(), N->data.end(), seeds[0]));
		N->data.erase(remove(N->data.begin(), N->data.end(), seeds[1]));
		G1.push_back(seeds[0]);
		G2.push_back(seeds[1]);
		/*cout <<"G1[0]" << G1[0] << endl;
		cout << "G2[0]" << G2[0] << endl;*/

		while (true) {
			if (N->data.size() <= 0)
				break;

			if ((int)min(G1.size(), G2.size()) + N->data.size() - (int)max(G1.size(), G2.size()) <= Min_entries) {
				if (G1.size() < G2.size())
					G1.insert(G1.end(), N->data.begin(), N->data.end());
				else
					G2.insert(G2.end(), N->data.begin(), N->data.end());
				N->data.clear();
			}
			else {

				R_Tree::_pick_next_leaf(N->data, G1, G2);
			}

		}
		if (N->parent != nullptr)
			N->parent->children.erase(remove(N->parent->children.begin(), N->parent->children.end(), N));

		//for (int i = 0; i < G1.size(); i++) {
		//	cout << "G1 " << i << ' ' << G1[i] << endl;
		//}
		//for (int i = 0; i < G2.size(); i++) {
		//	cout << "G2 " << i << ' ' << G2[i] << endl;
		//}


		result[0] = new R_Tree::Node(false, true);
		result[0]->data = G1;
		result[0]->rect = R_Tree::adjust_rect(result[0]);
		result[0]->parent = N->parent;
		result[1] = new R_Tree::Node(false, true);
		result[1]->data = G2;
		result[1]->rect = R_Tree::adjust_rect(result[1]);
		result[1]->parent = N->parent;
		delete N;

	}
	return result;


}

void R_Tree::_find_leaf(Node* N, Rect rect, Node* result)
{
	result = nullptr;
	if (N->is_leaf) {
		for (int i = 0; i < N->data.size(); i++) {
			if (N->data[i] == rect)
				result = N;
		}

	}
	else {
		for (int i = 0; i < N->children.size(); i++) {
			if (Rect::is_overlap(N->children[i]->rect, rect))
				_find_leaf(N->children[i], rect, result);
		}
	}
}













R_Tree::Node::Node(bool is_root, bool is_leaf)
{
	this->is_root = is_root;
	this->is_leaf = is_leaf;
	this->parent = nullptr;
}

bool R_Tree::Node::is_full()
{
	if (is_leaf)
		return this->data.size() >= Max_entries;
	return this->children.size() >= Max_entries;
}

void R_Tree::Node::insert(Rect rect)
{
	data.push_back(rect);
}



Rect R_Tree::adjust_rect(R_Tree::Node* N)
{
	Rect new_rect;
	if (N->is_leaf) {
		new_rect = N->data[0];
		for (int i = 1; i < N->data.size(); i++) {
			new_rect = Rect::marged_rect(new_rect, N->data[i]);
		}
	}
	else {
		new_rect = N->children[0]->rect;
		for (int i = 1; i < N->children.size(); i++) {
			new_rect = Rect::marged_rect(new_rect, N->children[i]->rect);
		}
	}
	return new_rect;
}

void R_Tree::_condense_tree(Node* leaf)
{
	Node* N = leaf;
	vector<Node*> Q;
	while (true) {
		if (!N->is_root) {
			Node* P = N->parent;
			if (N->_is_fewer_m()) {
				Q.push_back(N);
				P->children.erase(remove(P->children.begin(), P->children.end(), N));
			}
			else {
				N->rect = R_Tree::adjust_rect(N);
			}
		}
		else {
			break;
		}
	}
	for (int i = 0; i < Q.size(); i++) {
		if (Q[i]->is_leaf) {
			for (int j = 0; i < Q[i]->data.size(); j++) {
				R_Tree::_insert(Q[i]->data[j]);
			}
		}
		else {
			/*must be placed higher in the tree,
			so that leaves of ther dependet
			subtrees will be on the same level leaves of the main tree */
		}
	}


}
bool R_Tree::Node::_is_fewer_m() {
	if (this->is_leaf)
		return this->data.size() < Min_entries;
	return this->children.size() < Min_entries;
}

void R_Tree::Node::_print_tree(string t, bool last)
{
	cout << t;
	if (last) {
		cout << "\\-";
		t += "  ";
	}
	else {
		cout << "|-";
		t += "|  ";
	}
	cout << rect << endl;
	if (is_leaf) {
		for (int i = 0; i < data.size(); i++)
            if(i==data.size()-1) {

                if (data[i].get_lt() == data[i].get_rb())
                cout << t << "\\-" << Rect::to_str(data[i].get_lt())<< endl;
                else
                    cout<< t << "\\-" << data[i] <<endl;
                t += ' ';
            }
            else
            if (data[i].get_lt() == data[i].get_rb())
                cout << t << "|-" << Rect::to_str(data[i].get_lt())<< endl;
            else
                cout<< t << "|-" << data[i] <<endl;
	}
	else {
		t += "  ";
		for (int i = 0; i < children.size(); i++)
			children[i]->_print_tree(t, i == children.size() - 1);

	}

}

void R_Tree::Node::height(int& res)
{
	res += 1;
	if (is_leaf)
		return;
	children[0]->height(res);

}

Rect* R_Tree::_pick_seeds_leaf(vector<Rect> data)
{
	Rect* res = new Rect[2];
	double max_marge_area = -1;
	for (int i = 0; i < data.size(); i++) {
		for (int j = i; j < data.size(); j++) {
			if (Rect::area_to_increase(data[i], data[j]) > max_marge_area and i != j) {
				max_marge_area = Rect::area_to_increase(data[i], data[j]);
				res[0] = data[i];
				res[1] = data[j];
			}


		}
	}

	return res;
}
R_Tree::Node** R_Tree::_pick_seeds(vector<Node*> children)
{
	R_Tree::Node** res = new R_Tree::Node * [2];
	double max_marge_area = -1;
	for (int i = 0; i < children.size(); i++) {
		for (int j = i; j < children.size(); j++) {
			if (Rect::area_to_increase(children[i]->rect, children[j]->rect) > max_marge_area and i != j) {
				max_marge_area = Rect::area_to_increase(children[i]->rect, children[j]->rect);
				res[0] = children[i];
				res[1] = children[j];
			}


		}
	}
	return res;
}

void R_Tree::_pick_next(vector<Node*>& N, vector<Node*>& G1, vector<Node*>& G2)
{
	double max_area_dif = -1;
	vector<Node*>* min_area = &G1;
	Node* node_to_instr = N[0];
	for (int i = 0; i < N.size(); i++) {
		double G1_area = _resulting_area(G1, N[i]);
		double G2_area = _resulting_area(G2, N[i]);
		if (abs(G2_area - G1_area) > max_area_dif) {
			max_area_dif = abs(G2_area - G1_area);
			node_to_instr = N[i];
			if (G1_area - _area(G1) < G2_area - _area(G2))
				min_area = &G1;
			else
				min_area = &G2;
		}
	}
	N.erase(remove(N.begin(), N.end(), node_to_instr));
	min_area->push_back(node_to_instr);



}


void R_Tree::_pick_next_leaf(vector<Rect>& R, vector<Rect>& S1, vector<Rect>& S2)
{
	double max_area_dif = -1;
	vector<Rect>* min_area = &S1;
	Rect node_to_instr = R[0];

	for (int i = 0; i < R.size(); i++) {
		double S1_area = _resulting_area(S1, R[i]);
		double S2_area = _resulting_area(S2, R[i]);
		if (abs(S2_area - S1_area) > max_area_dif) {
			max_area_dif = abs(S2_area - S1_area);
			node_to_instr = R[i];
			if (S1_area - Rect::Area(S1) < S2_area - Rect::Area(S2))
				min_area = &S1;
			else
				min_area = &S2;
		}
	}
	R.erase(remove(R.begin(), R.end(), node_to_instr));
	min_area->push_back(node_to_instr);


}

double R_Tree::_resulting_area(vector<Node*> G, Node* N)
{
	double min_x = N->rect.get_lt().x;
	double max_x = N->rect.get_rb().x;
	double min_y = N->rect.get_lt().y;
	double max_y = N->rect.get_rb().y;
	for (int i = 0; i < G.size(); i++) {
		min_x = (double)min(G[i]->rect.get_lt().x, min_x);
		max_x = (double)max(G[i]->rect.get_rb().x, max_x);
		min_y = (double)min(G[i]->rect.get_lt().y, min_y);
		max_y = (double)max(G[i]->rect.get_rb().y, max_y);
	}
	return Rect(min_x, min_y, max_x, max_y).area();
}

double R_Tree::_resulting_area(vector<Rect> S, Rect N)
{
	double min_x = N.get_lt().x;
	double max_x = N.get_rb().x;
	double min_y = N.get_lt().y;
	double max_y = N.get_rb().y;
	for (int i = 0; i < S.size(); i++) {
		min_x = (double)min(S[i].get_lt().x, min_x);
		max_x = (double)max(S[i].get_rb().x, max_x);
		min_y = (double)min(S[i].get_lt().y, min_y);
		max_y = (double)max(S[i].get_rb().y, max_y);
	}
	return Rect(min_x, min_y, max_x, max_y).area();
}

double R_Tree::_area(vector<Node*> N)
{

	double min_x = N[0]->rect.get_lt().x;
	double max_x = N[0]->rect.get_rb().x;
	double min_y = N[0]->rect.get_lt().y;
	double max_y = N[0]->rect.get_rb().y;
	for (int i = 1; i < N.size(); i++) {
		min_x = (double)min(N[i]->rect.get_lt().x, min_x);
		max_x = (double)max(N[i]->rect.get_rb().x, max_x);
		min_y = (double)min(N[i]->rect.get_lt().y, min_y);
		max_y = (double)max(N[i]->rect.get_rb().y, max_y);
	}
	return Rect(min_x, min_y, max_x, max_y).area();
}


string R_Tree::to_string(){
    map<Node*, int> m = {{root,0}};
    string res = "";
    R_Tree::node_to_string(res,root,m);
    return  res;
}

void R_Tree::node_to_string(string &s, Node *N, map<Node*,int>& m) {
    int level = m[N->parent];
    m[N] = level+1;
    s+= std::to_string(level)+' '+N->rect.to_string()+"\n";

    if(N->is_leaf) {
        level +=1;
        for (int i = 0; i < N->data.size(); i++)
            s+=std::to_string(level)+' '+N->data[i].to_string()+"\n";
    }
    else{
        for (int i = 0; i < N->children.size(); i++)
            R_Tree::node_to_string(s,N->children[i],m);

    }
}

void R_Tree::_contain(Node* T, Rect R,vector<Rect>& result){
    if (!T->is_leaf) {
        for (int i = 0; i < T->children.size(); i++) {
            if (Rect::is_overlap(T->children[i]->rect, R))
                R_Tree::_contain(T->children[i],R,result);

        }
    }
    else {
        for (int i = 0; i < T->data.size(); i++)
            if (T->data[i]==R)
                result.push_back(R);
    }

}
bool R_Tree::is_contain(Rect R){
    vector<Rect> res;
    _contain(root,R,res);
    return res.size() >= 1;
}
Rect R_Tree::get_root(){
    return this->root->rect;
}

void R_Tree::_nn(Node* T,Rect R, vector<Rect>& res,double* best){
    if (!T->is_leaf) {
        for (int i = 0; i < T->children.size(); i++) {
            R_Tree::_nn(T->children[i],R,res,best);

        }
    }
    else {
        for (int i = 0; i < T->data.size(); i++) {
            auto lt = T->data[i].get_lt();
            if (*best >= Rect::distance(lt,R.get_lt())) {
                res.push_back(T->data[i]);
                *best = Rect::distance(lt, R.get_lt());
            }

        }
    }

}
vector<Rect> R_Tree::nn(Rect R){
    vector<Rect> res;
    vector<Rect> result;
    double *best = new double(99999);
    R_Tree::_nn(root,R,res,best);
    for(int i = res.size()-1;i>=0; i--){
        if (Rect::distance(R.get_lt(), res[i].get_lt()) == *best){
            result.push_back(res[i]);
        }
        else
            break;


    }
    return result;


}