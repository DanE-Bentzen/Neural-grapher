import graphviz


class NeuralGraph:
    def __init__(self, number_of_inputs, number_of_outputs, hidden_layers= None, filename = None):
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.hidden_layers = hidden_layers
        self.filename = filename

        # creates indexed matrix for all hidden layers 
        try:
            if self.hidden_layers is not None:
                self.hidden_layers_list = []
                for index, hidden_layer in enumerate(self.hidden_layers):
                    list_of_nodes = []
                    for node_index in range(1, hidden_layer + 1):
                        list_of_nodes.append(f'H{index+1},{node_index}')
                    self.hidden_layers_list.append(list_of_nodes)
                
                    
        except TypeError:
            print("'hidden_layers' must be a list with parameters [size_layer_1, size_layer_2,...,size_layer_k].")
            
            
        self.graph_object = graphviz.Digraph(filename = self.filename, format = 'png', 
                                             directory = './neural_plots/', engine='dot')
        
        
        # randir=LR Starts graph from left to right. ranksep=2 separates nodes in horizontal direction. nodesep=1 separates nodes in vertical direction  splines='false',
        self.graph_object.attr(rankdir = 'LR', ranksep='7', nodesep='1', arrowsize = '0.2',  labelsep ='1', labelfloat ='true', wheight = '-1') 
    def input_layers(self):
        """
        Method creates graphic object for each input node in the neural network. 
        The nodes are indexed in interval [1, number_of_inputs]
        param:,
            (obj: 'int') 
        """
        print('entered: input_layers')
        with self.graph_object.subgraph(name = 'Inputs') as In:
            In.attr('node', shape='doublecircle')
            [In.node(f'I{node_index}',f'x{node_index}') for node_index in range(1, self.number_of_inputs + 1)]



    def output_layers(self):
        """
        Method creates graphic object for each output node in the neural network. 
        If: no hidden layers output nodes will be indexed in interval [number_of_inputs+1, number_of_outputs]
        else:  
            param:
            (obj: 'int') 
        """
        print('entered: output_layers')
        with self.graph_object.subgraph(name = 'Output') as Out:
            Out.attr('node', shape='doublecircle')
            [Out.node(f'O{index}', f'y{index}') for index in range(1, self.number_of_outputs + 1)]

    def hidden_layer(self):
        """
        Method creates graphic object for each node in each hidden layer.
        """
        print('entered: hidden_layers')
        if self.hidden_layers is None:
            print('No hidden layers...')
            pass
        else:
            with self.graph_object.subgraph(name = 'Hidden') as Hidden:
                Hidden.attr('node', shape='circle', color = 'lightgrey')
                for layer in self.hidden_layers_list:
                    [Hidden.node(nodes, str(label+1)) for label, nodes in enumerate(layer)]
                        
    def counter(self, x, y):
        if x==1 and y ==1:
            return 1
        elif x==2 and y==1:
            return 3
        elif x==1 and y==2:
            return 2
        else:
            return 4

    def egdes_(self):
        """
        Method creates arrows from nodes to left onto node right. 
        If there is not chosen any hidden layers, method connects arrows directly from input layer to output layer
        """
        print('entered: egdes')
        if self.hidden_layers is None:
            [self.graph_object.edge(f'I{a}', f'O{b}') for a in range(1, self.number_of_inputs + 1) for b in range(1, self.number_of_outputs +1)]
        
        else:
            [self.graph_object.edge(f'I{a}', b) for a in range(1, self.number_of_inputs +1) for b in self.hidden_layers_list[0]]
            
            for i in range(len(self.hidden_layers)):
                try:
                    [self.graph_object.edge(a, b) for a in self.hidden_layers_list[i] for b in self.hidden_layers_list[i+1]]
                except IndexError:
                    print('List out of range. This is expected.')
                    pass
            [self.graph_object.edge(a, f'O{b}') for a in self.hidden_layers_list[-1] for b in range(1, self.number_of_outputs + 1)]
            

    def make_graph(self):
        print('entered: make_graph')
        self.input_layers()
        self.output_layers()
        self.hidden_layer()
        self.egdes_()
        picture = self.graph_object
        self.graph_object.view(quiet = True)

neural_object = NeuralGraph(number_of_inputs = 6, number_of_outputs = 6, hidden_layers = [10, 32, 32, 2], filename='neural6')
neural_object.make_graph()
#print(neural_object)>


from IPython.display import Image
Image(filename='./neural_plots/neural6.png') 




