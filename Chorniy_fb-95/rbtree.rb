class Node    
    attr_accessor :key, :value, :left, :right, :parent, :color

    def initialize(key, calue)
        @key = key
        @value = value  
        @parent = nil 
        @left = nil 
        @right = nil 
        @color = 1 
    end
end

class Tree
    
    attr_accessor :TNULL, :root

    def initialize()
        @TNULL = Node.new(0, 0)
        @TNULL.color = 0
        @TNULL.left = nil
        @TNULL.right = nil
        @root = @TNULL
    end

    def insert(key, value) 
        
        node = Node.new(key, value)
        node.parent = nil
        node.value = value
        node.left = @TNULL
        node.right = @TNULL
        node.color = 1 
        
        node2 = nil
        node1 = @root
        
        while node1 != @TNULL 
            node2 = node1
            if node.value < node1.value 
                node1 = node1.left
            else
                node1 = node1.right
            end
        end
               
        node.parent = node2

        if node2 == nil 
            @root = node
        elsif node.value < node2.value 
            node2.left = node
        else
            node2.right = node
        end
        
        if node.parent == nil 
            node.color = 0
            return
        end
        
        if node.parent.parent == nil 
            return
        end
        
        while node.parent.color == 1 
            if node.parent == node.parent.parent.right 
                node1 = node.parent.parent.left 
                if node1.color == 1 
                    
                    node1.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else
                    if node == node.parent.left 
                        
                        node = node.parent
                        right_rotate(node)
                    end
                    
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    left_rotate(node.parent.parent)
                end
            else
                node1 = node.parent.parent.right 
                
                if node1.color == 1 
                    
                    node1.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent 
                else
                    if node == node.parent.right 
                        
                        node = node.parent
                        left_rotate(node)
                    end
                    
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    right_rotate(node.parent.parent)
                end
            end
            if node == @root 
                break
            end
        end
        @root.color = 0

    end

    def search(node, value) 
        if node == @TNULL || value == node.value 
            return node
        end
        
        if value < node.value 
            return search(node.left, value)
        end
        return search(node.right, value)
    end

    def getkey(node) 
        return search(@root, node)
    end  

    def delhelper(node, value) 
        
        node3 = @TNULL
        while node != @TNULL 
            if node.value == value 
                node3 = node
            end
            
            if node.value <= value 
                node = node.right
            else
                node = node.left
            end
        end
        
        if node3 == @TNULL 
            puts("Couldn't find value in the tree")
            return
        end
        
        node2 = node3
        y_original_color = node2.color
        if node3.left == @TNULL 
            node1 = node3.right
            swap(node3, node3.right)
        elsif (node3.right == @TNULL) 
            node1 = node3.left
            swap(node3, node3.left)
        else
            node2 = minimum(node3.right)
            y_original_color = node2.color
            node1 = node2.right
            if node2.parent == node3 
                node1.parent = node2
            else
                swap(node2, node2.right)
                node2.right = node3.right
                node2.right.parent = node2
            end
            
            swap(node3, node2)
            node2.left = node3.left
            node2.left.parent = node2
            node2.color = node3.color
        end
        if y_original_color == 0 
        while node1 != @root && node1.color == 0 
            if node1 == node1.parent.left 
                nodep = node1.parent.right
                if nodep.color == 1 
                    
                    nodep.color = 0
                    node1.parent.color = 1
                    left_rotate(node1.parent)
                    nodep = node1.parent.right
                end
                
                if nodep.left.color == 0 && nodep.right.color == 0 
                    
                    nodep.color = 1
                    node1 = node1.parent
                else
                    if nodep.right.color == 0 
                        
                        nodep.left.color = 0
                        nodep.color = 1
                        right_rotate(nodep)
                        nodep = node1.parent.right
                    end
                    
                    
                    nodep.color = node1.parent.color
                    node1.parent.color = 0
                    nodep.right.color = 0
                    left_rotate(node1.parent)
                    node1 = @root
                end
            else
                nodep = node1.parent.left
                if nodep.color == 1 
                    
                    nodep.color = 0
                    node1.parent.color = 1
                    right_rotate(node1.parent)
                    nodep = node1.parent.left
                end
                
                if nodep.left.color == 0 && nodep.right.color == 0 
                    
                    nodep.color = 1
                    node1 = node1.parent
                else
                    if nodep.left.color == 0 
                        
                        nodep.right.color = 0
                        nodep.color = 1
                        left_rotate(nodep)
                        nodep = node1.parent.left 
                    end
                    
                    
                    nodep.color = node1.parent.color
                    node1.parent.color = 0
                    nodep.left.color = 0
                    right_rotate(node1.parent)
                    node1 = @root
                end
            end
        end
        node1.color = 0
        end
    end 

    def delete_node(value) 
        delhelper(@root, value)
    end

    def swap(node1, node2) 
        if node1.parent == nil 
            @root = node2
        elsif node1 == node1.parent.left 
            node1.parent.left = node2
        else
            node1.parent.right = node2
        end
        node2.parent = node1.parent
    end
    
    def minimum(node) 
        while node.left != @TNULL 
            node = node.left
        end
        return node
    end   
    
    def left_rotate(node1) 
        node2 = node1.right
        node1.right = node2.left
        if node2.left != @TNULL 
            node2.left.parent = node1
        end
        
        node2.parent = node1.parent
        if node1.parent == nil 
            @root = node2
        elsif node1 == node1.parent.left 
            node1.parent.left = node2
        else
            node1.parent.right = node2
        end
        node2.left = node1
        node1.parent = node2
    end
      
    def right_rotate(node1) 
        node2 = node1.left
        node1.left = node2.right
        if node2.right != @TNULL 
            node2.right.parent = node1
        end
        
        node2.parent = node1.parent
        if node1.parent == nil 
            @root = node2
        elsif node1 == node1.parent.right 
            node1.parent.right = node2
        else
            node1.parent.left = node2
        end
        node2.right = node1
        node1.parent = node2
    end
    
end

class Table
    attr_accessor :name, :cols, :values, :forest, :head
    @@counter = 1
    
    def initialize(name, cols)
        @name = name
        @cols = cols
        @forest = {}
        @head = {}
        cols.each do |c|
            @forest[name + c] = Tree.new()
        end
    end

    def insert(name, values)
        @head[@@counter] = values
        values.each do |c|
            c = c.codepoints.join.to_i
        end
        if @cols.length != values.length
            puts 'error' 
        else
            for col in 0..cols.length() - 1
                @forest[name + @cols[col]].insert(@@counter, values[col])
            end
        end
        @@counter += 1
    end

    def getbykey(key)
        p @head[key]
    end

end

# bst = Tree.new
# bst.insert(1, 8)
# bst.insert(2, 18)
# bst.insert(3, 5)
# bst.insert(4, 15)
# bst.insert(5, 17)
# bst.insert(6, 25)
# bst.insert(7, 40)
# bst.insert(8, 80)
# bst.delete_node(25)

# puts bst.getkey(7).left.value
# puts bst.getkey(7).right.value

testname = 'cats'
testcols = ['name', 'color', 'food']
test2cols = ['name', 'color', 'food', 'zhopa']
testvalues = ['zhizha', 'green', 'pizza']
test2values = ['matylda', 'blue', 'sushi']

testtable = Table.new(testname, testcols)

# testtable.forest.each do |c|
#     c[1].insert(1, 8)
#     c[1].insert(2, 18)
#     c[1].insert(3, 5)
#     c[1].insert(4, 15)
#     c[1].insert(5, 17)
#     c[1].insert(6, 25)
#     c[1].insert(7, 40)
#     c[1].insert(8, 80)
#     c[1].delete_node(25)
# end


#pp testtable.cols

testtable.insert(testname, testvalues)
testtable.insert(testname, test2values)
# testtable.forest.each do |c|
#     pp c
#     puts '----------'
# end
pp testtable.forest['catsname'].getkey('matylda').key
# pp testtable.forest['catsname'].getkey(8).right.value
#pp testtable.forest['catsname']

pp testtable.head

testtable.getbykey(2)

# testtable.forest.each do |c|
#     pp c[1].root
#     puts '---------------'
# end