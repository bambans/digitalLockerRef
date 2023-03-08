from rdflib import Graph
from rdflib.query import Result
from ast import AST
import ast

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

def tokenTranslate(astClassNode:AST, alt:bool = False) -> str:
    """
    This method receives an AST node and returns its python token version for that tokenizable nodes. It supports the following arguments:
    - `astClassNode:AST`: an AST node;
    - `alt:bool`: a boolean variable which makes possible to change what token string will be returned.
    """
    astToTokenList = {
        ast.AST: '',
        ast.mod: '',
        ast.Module: '',
        ast.Interactive: '',
        ast.Expression: '',
        ast.FunctionType: '',
        ast.Suite: '',
        ast.stmt: '',
        ast.FunctionDef: 'def {}',
        ast.AsyncFunctionDef: 'async def',
        ast.ClassDef: 'class',
        ast.Return: 'return',
        ast.Delete: '',
        ast.Assign: '',
        ast.AugAssign: '',
        ast.AnnAssign: '',
        ast.For: 'for',
        ast.AsyncFor: '',
        ast.While: 'while',
        ast.If: 'if',
        ast.With: 'with',
        ast.AsyncWith: '',
        ast.Match: 'match',
        ast.Raise: 'raise',
        ast.Try: 'try',
        ast.TryStar: '',
        ast.Assert: 'assert',
        ast.Import: 'import',
        ast.ImportFrom: 'from {} import {}' if not alt else 'from {} import {} as {}' ,
        ast.Global: 'global',
        ast.Nonlocal: '',
        ast.Expr: '',
        ast.Pass: 'pass',
        ast.Break: 'break',
        ast.Continue: 'continue',
        ast.expr: '',
        ast.BoolOp: '',
        ast.NamedExpr: '',
        ast.BinOp: '',
        ast.UnaryOp: '',
        ast.Lambda: 'lambda',
        ast.IfExp: '',
        ast.Dict: 'dict',
        ast.Set: '{}',
        ast.ListComp: '',
        ast.SetComp: '',
        ast.DictComp: '',
        ast.GeneratorExp: '',
        ast.Await: 'await',
        ast.Yield: 'yield',
        ast.YieldFrom: 'yield from',
        ast.Compare: '',
        ast.Call: '',
        ast.FormattedValue: '',
        ast.JoinedStr: '',
        ast.Constant: '',
        ast.Num: '',
        ast.Str: '',
        ast.Bytes: '',
        ast.NameConstant: '',
        ast.Ellipsis: '',
        ast.Attribute: '',
        ast.Subscript: '',
        ast.Starred: '',
        ast.Name: '',
        ast.List: '[{}]',
        ast.Tuple: '({})',
        ast.Slice: '',
        ast.expr_context: '',
        ast.Load: '',
        ast.Store: '',
        ast.Del: '',
        ast.AugLoad: '',
        ast.AugStore: '',
        ast.Param: '',
        ast.boolop: '',
        ast.And: 'and',
        ast.Or: 'or',
        ast.operator: '',
        ast.Add: '+',
        ast.Sub: '-',
        ast.Mult: '*',
        ast.MatMult: '@',
        ast.Div: '/',
        ast.Mod: '%',
        ast.Pow: '**',
        ast.LShift: '',
        ast.RShift: '',
        ast.BitOr: '',
        ast.BitXor: '',
        ast.BitAnd: '',
        ast.FloorDiv: '',
        ast.unaryop: '',
        ast.Invert: '',
        ast.Not: 'not',
        ast.UAdd: '',
        ast.USub: '',
        ast.cmpop: '',
        ast.Eq: '==',
        ast.NotEq: '!=',
        ast.Lt: '<',
        ast.LtE: '<=',
        ast.Gt: '>',
        ast.GtE: '>=',
        ast.Is: 'is',
        ast.IsNot: 'is not',
        ast.In: 'in',
        ast.NotIn: 'not in',
        ast.comprehension: '',
        ast.excepthandler: '',
        ast.ExceptHandler: '',
        ast.arguments: '',
        ast.arg: '',
        ast.keyword: '',
        ast.alias: '',
        ast.withitem: '',
        ast.match_case: '',
        ast.pattern: '',
        ast.MatchValue: '',
        ast.MatchSingleton: '',
        ast.MatchSequence: '',
        ast.MatchMapping: '',
        ast.MatchClass: '',
        ast.MatchStar: '',
        ast.MatchAs: '',
        ast.MatchOr: '',
        ast.type_ignore: '',
        ast.TypeIgnore: '',
        ast.slice: '',
        ast.Index: '',
        ast.ExtSlice: ''
    }
    return astToTokenList[astClassNode]
    # point = {'x':4,'y':-5}
    # print('{xx} {y}'.format_map(point))

    # point = {'x':4,'y':-5, 'z': 0}
    # print('{x} {y} {z}'.format_map(point))

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
            print(level*"    ", f'name: {tokenTranslate(astClassNode = treeNode) or subject.s.fragment}')
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
                    print(level*"    ", f'name: {tokenTranslate(astClassNode = ASTlist[subject.o.fragment]) or subject.o.fragment}')
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
