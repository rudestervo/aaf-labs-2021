#pragma once
#include "Rect.h"
#include <vector>
#include <string>
#include <algorithm>
#include <map>



using namespace std;



class R_Tree
{
public:
	R_Tree();
	void incert(Rect rect);
	vector<Rect> search(Rect rect);
	void print_tree();
	int get_height();
	void test();
    string to_string();
    bool is_contain(Rect R);
    Rect get_root();
    vector<Rect> nn(Rect R);

    class Node {
    public:
        bool is_leaf;
        bool is_root;
        Node* parent;
        vector<Node*> children;
        vector<Rect> data;
        Rect rect;
        Node(bool is_root, bool is_leaf);
        bool is_full();
        void insert(Rect rect);
        bool _is_fewer_m();
        void _print_tree(string t, bool last);
        void height(int& res);



    };





private:

	

	Node* root;
	static const int Max_entries = 2;
	static const int Min_entries = 1;

	void _search(Rect rect, Node* T, vector<Rect>& result);
	void _insert(Rect rect);
	Node* _choose_leaf(Rect rect);
	void _adjust_tree(Node* L1,Node* L2);
	Node* _choose_subtree(Node* N, Rect rect);
	void _delete(Rect rect);
	Node** _split_node(Node* N);
	void _find_leaf (Node* N, Rect rect, Node* result);
	Rect adjust_rect(R_Tree::Node* N);
	void _condense_tree(Node* N);
	Rect* _pick_seeds_leaf(vector<Rect> data);
	Node** _pick_seeds(vector<Node*> children);
	void _pick_next(vector<Node*>& N, vector<Node*>& G1, vector<Node*>& G2);
	void _pick_next_leaf(vector<Rect>& R, vector<Rect>& S1, vector<Rect>& S2);
	double _resulting_area(vector<Node*> G, Node* N);
	double _resulting_area(vector<Rect> S, Rect N);
	double _area(vector<Node*> N);
    void _contain(Node* T, Rect R,vector<Rect>& result);
    static void node_to_string(string &s, Node *N, map<Node*,int>& m);
    void _nn(Node* T,Rect R, vector<Rect>& res,double* best);














};



