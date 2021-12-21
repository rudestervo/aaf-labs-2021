#include "Collection.h"
#include <stack>

Set UniSets(Set f_set, Set s_set) {
    return f_set.Union(s_set);
}

bool IsLeaf(Node* node) {
    if (node->subnodes[0] == nullptr && node->subnodes[1] == nullptr)
    {
        return true;
    }
    return false;
}




void Collection::PrintSubtree(std::ostream& os, Node* subtree_root, std::string prefix, std::string children_prefix) const {
    if (subtree_root == nullptr) {
        return;
    }
    os << prefix << subtree_root->set << std::endl;

    PrintSubtree(os, subtree_root->subnodes[0], children_prefix + "L-- ", children_prefix + "|   ");
    PrintSubtree(os, subtree_root->subnodes[1], children_prefix + "L-- ", children_prefix + "    ");
}

void Collection::Print(std::ostream& os) const {
    if (!root) {
        os << "Empty Collection";
        return;
    }

    PrintSubtree(os, root, "", "");

}

bool Collection::Contains(const Set& set_to_check) {
    if (!root)
    {
        return false;
    }
    bool res = root->Contains(set_to_check);
    return res;
}

std::vector<Set> Collection::Contained_By(Set superset) {
    if (!root)
    {
        return {};
    }

    std::vector<Set> res;

    return this->root->Contained_By(res, superset);
}


std::vector<Set> Node::Contained_By(std::vector<Set>& res, Set superset) {


    if (IsLeaf(this))
    {
        if (set.IsSubsetOf(superset))
        {
            res.push_back(set);
        }
        
        return res;
    }

    if ((set.data.size() - set.Minus(superset).data.size()) == set.data.size())
    {
        return {};
    }


    subnodes[0]->Contained_By(res, superset);
    subnodes[1]->Contained_By(res, superset);

    return res;
}

std::vector<Set> Collection::Contains_Search(Set subset) {
    if (!root)
    {
        return {};
    }

    std::vector<Set> res;

    return this->root->Contains_Search(res, subset);
}

std::vector<Set> Node::Contains_Search(std::vector<Set>& res, Set subset) {
    

    if (IsLeaf(this))
    {
        res.push_back(set);
        return res;
    }
    
    if (subset.IsSubsetOf(subnodes[0]->set)) {
       
        subnodes[0]->Contains_Search(res, subset);
    }
    
    if (subnodes[1] != nullptr && subset.IsSubsetOf(subnodes[1]->set)) {

        subnodes[1]->Contains_Search(res, subset);
    }

    return res;
}


std::vector<Set> Collection::Intersects(Set intersec_set) {
    if (!root)
    {
        return {};
    }

    std::vector<Set> res;
    
    return this->root->Intersects(res, intersec_set);
}

std::vector<Set> Node::Intersects(std::vector<Set>& res, Set intersec_set) {

    if (IsLeaf(this))
    {
        if ((set.data.size() - set.Minus(intersec_set).data.size()) > 0)
        {
            res.push_back(set);
            return res;
        }
    }

    if ((set.data.size() - set.Minus(intersec_set).data.size()) > 0)
    {
        subnodes[0]->Intersects(res, intersec_set);

        if (subnodes[1] != nullptr)
        {
            subnodes[1]->Intersects(res, intersec_set);
        }
    }
   
    return res;
}


std::vector<Set> Collection::Search() {

    if (!root)
    {
        return {};
    }
    
    std::vector<Set> res;

    return this->root->Search(res);

}

std::vector<Set> Node::Search(std::vector<Set>& res) {

    if (this->subnodes[0])
    {
        this->subnodes[0]->Search(res);
       
    }
    if (this->subnodes[1])
    {
        this->subnodes[1]->Search(res);
        
    }
    
    if (IsLeaf(this))
    {
        res.push_back(this->set);
    }
 
    return res;
}

bool Node::Contains(const Set& set_to_check) {
  
    if (IsLeaf(this))
    {
        if (set.IsSubsetOf(set_to_check))
        {
            return true;
        };
        return false;
    }
    
    bool found = false;
    
    if (set_to_check.IsSubsetOf(subnodes[0]->set))
    {
        found = subnodes[0]->Contains(set_to_check);
    };
    
    if (subnodes[1] && !found && set_to_check.IsSubsetOf(subnodes[1]->set))
    {
       found = subnodes[1]->Contains(set_to_check);
    };

    return found;

}


   

void Collection::Insert(const Set& new_set) {
    if (!root) { 
        root = new Node(nullptr, new_set);
        root->is_real = false;
        root->subnodes[0] = new Node(root, new_set);
        return;
    }
    root->ExpandTo(new_set);
    return root->Insert(new_set);
}

void Node::Insert(const Set& new_set) {
    // Step 0: check if Node is empty.

    if (subnodes[0] == nullptr) {
        // No subnodes at all. Just add the first subnode.
        subnodes[0] = new Node(this, new_set);
        subnodes[1] = new Node(this,set);
        ExpandTo(new_set);
        return;
    }

    if (subnodes[1] == nullptr) {
        // just insert as new subnode
        subnodes[1] = new Node(this, new_set);
        return;
    }
    this->ExpandTo(new_set);
    // Step 1: find MIN{new_set \ subnode[i]}
    //    It will show, how much do we need to expand a node to fit the set in it

    short argmin_i;
    Set complements[2] = {
        new_set.Minus(subnodes[0]->set),
        (subnodes[1] != nullptr) ? new_set.Minus(subnodes[1]->set) : Set(),
    };
    size_t complement_sizes[2] = {
        complements[0].Size(),
        complements[1].Size()
    };


    // Step 2: Subset test
    //     because (|X\A| = 0) => (X is a subset of A)

    if (complement_sizes[0] == 0) {
        subnodes[0]->Insert(new_set);
        return;
    }

    if (complement_sizes[1] == 0) {
        // set <= subnode[1]
        subnodes[1]->Insert(new_set);
        return;
    }
    
    // Step 3: General insert

    if (complement_sizes[0] <= complement_sizes[1]) {
        argmin_i = 0;
    }
    else {
        argmin_i = 1;
    }
    subnodes[argmin_i]->Insert(new_set);
    return;
}

    /* Returns a bitmask of subnodes, where `set` does fit:
    *    0 = 00b -  No subnode is a SUPERSET of `set`
    *    1 = 01b - set <= subnode[0]
    *    2 = 10b - set <= subnode[1]
    *    3 = 11b - set <= subnode[0], subnode[1]
    */
    unsigned int Node::superset_test(const Set & set) const {
        unsigned int mask = 0;
        if (subnodes[0] && set.IsSubsetOf(subnodes[0]->set)) {
            mask |= 1;
        }
        if (subnodes[1] && set.IsSubsetOf(subnodes[1]->set)) {
            mask |= 2;
        }
        return mask;
    }


/* Returns a bitmask of subnodes with subsets of `set`:
*    0 = 00b -  No subnode is a SUBSET of `set`
*    1 = 01b - subnode[0] <= set
*    2 = 10b - subnode[1] <= set
*    3 = 11b - subnode[0], subnode[1] <= set 
*/
unsigned int Node::subset_test(const Set& set) const {
    unsigned int mask = 0;
    if (subnodes[0] && subnodes[0]->set.IsSubsetOf(set)) {
        mask |= 1;
    }
    if (subnodes[1] && subnodes[1]->set.IsSubsetOf(set)) {
        mask |= 2;
    }
    return mask;
}

bool IsLeaf(const Node check_node) {
    if (check_node.subnodes[0] == nullptr && check_node.subnodes[1] == nullptr)
    {
        return true;
    }
    return false;
}


/*
Returns either the node is leaf or not
*/

void Node::ExpandTo(const Set& to_set) {
    set = set.Union(to_set);
}



