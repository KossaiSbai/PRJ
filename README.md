# PRJ


## Abstract
A **social network** can be defined as a structure connecting users with any kind of link such as friendship. In respect of social networks, one of the main problems to be solved and hence one of the main area of research, is finding the most influential nodes. This problem is called the **influence maximization problem**. Achieving this task can result tricky as the number of users gets bigger and bigger. The most common way to tackle this problem is to represent the social network as a graph where nodes represents users and edges denote the relationships between them. Using this graph representation approach, we can analyse a social network in order to find the most influential nodes. 
In this paper, the "enhanced degree centrality" approach [22] is extended for directed graphs. The implemented approach's performance is then analysed in two datasets and compared with several metric measures such as in-degree, out-degree and local clustering coefficient. By comparison, it is found that the nodes identified by the algorithm tend to have an overall better influence spread depending on the dataset. 

## Source code
The source code is split between two folders: [python](https://github.com/KossaiSbai/PRJ/tree/master/python) and [matlab](https://github.com/KossaiSbai/PRJ/tree/master/matlab).

### Python
The [python](https://github.com/KossaiSbai/PRJ/tree/master/python) folder contains all the Python code of the project. 
In fact the IM algorithm, the spreading models and an evaluation module to collect data results were implemented in Python.

### Matlab
The [matlab](https://github.com/KossaiSbai/PRJ/tree/master/matlab) folder contains all the Matlab code of the project. 
In fact Matlab is used to build the front end part of the project: visualise graphs in different configurations depending on the metric of interest. 


## Documentation
The [documentation](https://prj.readthedocs.io/en/latest/) of the source code for this project can be found in the [docs](https://github.com/KossaiSbai/PRJ/tree/master/docs) folder.
Both Python and Matlab documentations are hosted on Read the Docs and built using [Sphinx](https://www.sphinx-doc.org/en/master/). 

## Run the project 
In order to run the source code for this project, please carry out the following instructions: 
1. Clone the contents of this repository in an editor of your choice.
2. The Python part can be executed by running graph.py and evaluation.py
3. Regarding the Matlab part, open the file PRJ/matlab/PRJ.m and execute it via a Matlab editor such as [MATLAB_R2020a](https://www.mathworks.com/products/new_products/latest_features.html). 


The main method of graph.py does the following:
1. Reads a given file and creates a graph out of it.
2. Computes the most influential nodes of the graph by executing the IM algorithm.
3. Stores the returned nodes in a txt file called "influential_nodes.txt"
4. Carries out the diffusion process using a specific model such as Linear Threshold (LT)
5. The latter returns a list of influenced nodes.
6. Those are written to a txt file called "influenced_nodes.txt".

When open for the first time, graph.py will execute the previous steps for a randomly generated graph G stored in test_graph.txt. 

After the Python code is run, the three previously mentioned txt files contents get copied in the matlab folder.

Subsequently the Matlab code will display the various figures for a given graph data.

When open for the first time, PRJ.m executes on G as well.

The code will run on any graph stored as a txt or tgf file. 