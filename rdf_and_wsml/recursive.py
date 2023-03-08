from rdflib import Graph
from rdflib.query import Result
from ast import AST

pythonAST = Graph()
pythonAST.parse(location = 'rdfs/PythonAbstractSyntax.rdfs', format = 'xml')

# digital_locker_lib = Graph()
# digital_locker_lib.parse(location = 'rdfs/digitalLocker_librayRef.rdfs', format = 'xml')

digital_locker_ref = Graph()
digital_locker_ref.parse(location = 'rdfs/digitalLockerRefRef.rdfs', format = 'xml')

ASTlist = {}
"""
It is the default dictionary used in `astList` method. 
"""

def astList(node:AST = AST, list:dict = ASTlist):
    """
    This function maps all AST nodes into a dictionary in which we can get an object class inherit from <class 'ast'>.
    
    Ex.:
    - `ASTlist['AST'] = <class 'ast.AST'>`; 
    - `ASTlist['ExceptHandler'] = <class 'ast.ExceptHandler'>`.
    """
    list[node.__name__] = node
    subclasses = node.__subclasses__()
    for subclass in subclasses:
        astList(node = subclass)

def RDFQuery(graph:Graph, query:str) -> Result:
    """
    It performes a `rdflib.query` in a `rdflib.graph` and returns a `rdflib.query.Result`.
    """
    prefixes = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX mpl2kdl: <http://ufs.br/ontologies/mpl2kdl#>
        PREFIX cdt: <http://w3id.org/lindt/custom_datatypes#ucum>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    """
    return graph.query(prefixes+query)

def query(type = "SELECT", subject = "?s", predicate = "?p", object = "?o") -> str:
    """
    This function receives these following arguments (type and RDF semantic triple - subject, predicate and object) and it returns a SPARQL query string:
    - `type`: SELECT (default) or ASK;
    - `subject`: "?s" (default) or a given value;
    - `predicate`: "?p" (default) or a given value;
    - `object`: "?o" (default) or a given value.
    """
    if type == "SELECT":
        return """
            """+type+""" ?s ?p ?o WHERE{
                """+subject+""" """+predicate+""" """+object+""" .
            }
        """
    elif type == "ASK":
        return """
            """+type+"""{
                """+subject+""" """+predicate+""" """+object+""" .
            }
        """
    else:
        return None

def GraphRecursive(treeNode:AST|None = AST, graphNode = None, graph:Graph = pythonAST, level:int = 0):
    """
    This function walks recursively on the given RDFS graph. For each graph node, its type is tested and, from searching on `ASTlist`, it becomes possible to performe a new query for this node by each node field (described by the AST).
    
    This function needs these following arguments:
    - `treeNode:AST|None`: First node to dispacth subsequent queries on the RDFS graph;
    - `graphNode`: graph node for which will be perfomed its fields searching and the recursive subqueries;
    - `graph:Graph`: graph object in which will be performed all SPARQL queries;
    - `level:int`: level of the current recursion stack.
    """
    if treeNode is not None and graphNode is None:
        for subject in RDFQuery(graph, query(predicate = "rdf:type", object = "mpl2kdl:" + treeNode.__name__)):
            # print(level*"    ", "<<<<<", treeNode.__name__, ">>>>>")
            for field in treeNode._fields:
                for object in RDFQuery(graph, query(subject = "mpl2kdl:" + subject.s.fragment, predicate = "mpl2kdl:_" + field)):
                    # try:
                    #     print(level*"    ", treeNode.__name__, field, object.o.fragment)
                    # except:
                    #     print(level*"    ", treeNode.__name__, field, object.o)
                    GraphRecursive(treeNode = None, graphNode = object.o, graph = graph, level = level + 1)
    elif treeNode is None and graphNode is not None:
            try:
                for subject in RDFQuery(graph, query(subject = "mpl2kdl:" + graphNode.fragment, predicate="rdf:type")):
                    # print(level*"    ", "<<<<<", ASTlist[subject.o.fragment].__name__, ">>>>>")
                    for field in ASTlist[subject.o.fragment]._fields:
                        for object in RDFQuery(graph, query(subject = "mpl2kdl:" + graphNode.fragment, predicate = "mpl2kdl:_" + field)):
                            # try:
                            #     print(level*"    ", treeNode.__name__, field, object.o.fragment)
                            # except:
                            #     print(level*"    ", treeNode.__name__, field, object.o)
                            GraphRecursive(treeNode = None, graphNode = object.o, graph = graph, level = level + 1)
            except:
                print(level*"    ", graphNode)
    else:
        pass

def ASTRecursive(node:AST = AST, level:int = 0, graph:Graph = pythonAST):
    """
    In a recursive walking on AST, it performes `GraphRecursive()` for first leaf.
    """
    subclasses = node.__subclasses__()
    for subclass in subclasses:
        ASTRecursive(node = subclass, level = level+1, graph = graph)
        return
    if level > 1:   
        GraphRecursive(treeNode = node, graph = graph)
        return

def Recursive(node:AST = AST, graph:Graph = pythonAST):
    """
    This function only dispatch `ASTRecursive`.
    """
    ASTRecursive(node = node, graph = graph)


if __name__ == "__main__":
    astList()
    print("-------------------------- DIGITAL LOCKER REF -------------------------")
    Recursive(graph = digital_locker_ref)
    print("-----------------------------------------------------------------------")
