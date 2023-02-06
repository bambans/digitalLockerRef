from rdflib import Graph

digital_locker_lib = Graph()
digital_locker_lib.parse(location = 'rdfs/digitalLocker_librayRef.rdfs', format = 'xml')

digital_locker_ref = Graph()
digital_locker_ref.parse(location = 'rdfs/digitalLockerRefRef.rdfs', format = 'xml')

prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mpl2kdl: <http://ufs.br/ontologies/mpl2kdl#>

PREFIX  cdt: <http://w3id.org/lindt/custom_datatypes#ucum>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX   dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
"""

## It returns If's individuals
q = prefixes+"""
SELECT ?s ?p ?o WHERE{
    ?s rdf:type mpl2kdl:If .
}
"""

qres = digital_locker_ref.query(q)

code_line = ""
level = '   '

for qr in qres:
    code_line += "if "
    ## It returns Ifs' Compare objects
    qq = prefixes+"""
    SELECT ?s ?p ?o WHERE{
        mpl2kdl:"""+qr.s.fragment+""" mpl2kdl:_test ?o .
    }
    """
    qqres = digital_locker_ref.query(qq)
    for qqr in qqres:
        qqq_left = prefixes+"""
        SELECT ?s ?p ?o WHERE{
            mpl2kdl:"""+qqr.o.fragment+""" mpl2kdl:_left ?o .
        }
        """
        qqqres_left = digital_locker_ref.query(qqq_left)
        for qqqr in qqqres_left:
            q_left = prefixes+"""
            SELECT ?s ?p ?o WHERE{
                mpl2kdl:"""+qqqr.o.fragment+""" mpl2kdl:_id ?o .
            }
            """

            q_left_res = digital_locker_ref.query(q_left)
            for q_left in q_left_res:
                code_line += q_left.o+' '

        
        qqq_ops = prefixes+"""
        SELECT ?o WHERE{
            mpl2kdl:"""+qqr.o.fragment+""" mpl2kdl:_ops ?o .
        }
        """
        qqqres_ops = digital_locker_ref.query(qqq_ops)
        for qqqr in qqqres_ops:
            q_ops_ask = prefixes+"""
                ASK{
                    mpl2kdl:"""+qqqr.o.fragment+""" rdf:type mpl2kdl:Eq .
                }
                """
            q_ops_ask_res = digital_locker_ref.query(q_ops_ask)
            for ask_res in q_ops_ask_res:
                if ask_res == True:
                    code_line += "== "
        
        qqq_comparators = prefixes+"""
        SELECT ?s ?p ?o WHERE{
            mpl2kdl:"""+qqr.o.fragment+""" mpl2kdl:_comparators ?o .
        }
        """
        qqqres_comp = digital_locker_ref.query(qqq_comparators)
        for qqqr in qqqres_comp:
            q_comp_sel = prefixes+"""
            SELECT ?o WHERE{
                mpl2kdl:"""+qqqr.o.fragment+""" mpl2kdl:_value ?o .
            }
            """
            q_comp_res = digital_locker_ref.query(q_comp_sel)
            for q_comp in q_comp_res:
                code_line += q_comp.o
            code_line += f':\n'
        
        # getting body
        q_sel_body = prefixes+"""
        SELECT ?o WHERE{
            mpl2kdl:"""+qr.s.fragment+""" mpl2kdl:_body ?o .
        }
        """
        q_sel_body_res = digital_locker_ref.query(q_sel_body)
        for body in q_sel_body_res:
            q_sel_assing_targets = prefixes+"""
            SELECT ?o WHERE{
                mpl2kdl:"""+body.o.fragment+""" mpl2kdl:_targets ?o .
            }
            """
            q_sel_assing_targets = digital_locker_ref.query(q_sel_assing_targets)
            for target in q_sel_assing_targets:
                q_sel_name_id = prefixes+"""
                SELECT ?o WHERE{
                    mpl2kdl:"""+target.o.fragment+""" mpl2kdl:_id ?o .
                }
                """
                q_res_name_id = digital_locker_ref.query(q_sel_name_id)
                for id in q_res_name_id:
                    code_line += level+id.o+' '
            
            q_sel_assing_values = prefixes+"""
            SELECT ?o WHERE{
                mpl2kdl:"""+body.o.fragment+""" mpl2kdl:_value ?o .
            }
            """
            q_sel_assing_values = digital_locker_ref.query(q_sel_assing_values)
            for value in q_sel_assing_values:
                q_sel_call_func = prefixes+"""
                SELECT ?o WHERE{
                    mpl2kdl:"""+value.o.fragment+""" mpl2kdl:_func ?o .
                }
                """
                q_sel_call_funcs = digital_locker_ref.query(q_sel_call_func)
                for func in q_sel_call_funcs:
                    q_sel_func_name = prefixes+"""
                    SELECT ?o WHERE{
                        mpl2kdl:"""+func.o.fragment+""" mpl2kdl:_id ?o .
                    }
                    """
                    q_sel_func_name = digital_locker_ref.query(q_sel_func_name)
                    for name in q_sel_func_name:
                        code_line += "= "+name.o+"("
                
                # testar se existem argumentos para serem consultados
                q_ask_call_args = prefixes+"""
                ASK{
                    mpl2kdl:"""+value.o.fragment+""" mpl2kdl:_args ?o .
                }
                """
                q_ask_call_args = digital_locker_ref.query(q_ask_call_args)
                for ask in q_ask_call_args:
                    if ask == True:
                        q_sel_call_args = prefixes+"""
                        SELECT ?o WHERE{
                            mpl2kdl:"""+value.o.fragment+""" mpl2kdl:_args ?o .
                        }
                        """
                        q_sel_call_args = digital_locker_ref.query(q_sel_call_args)
                        for arg in q_sel_call_args:
                            q_sel_args_name = prefixes+"""
                            SELECT ?o WHERE{
                                mpl2kdl:"""+arg.o.fragment+""" mpl2kdl:_id ?o .
                            }
                            """
                            q_sel_args_name = digital_locker_ref.query(q_sel_args_name)
                            for name in q_sel_args_name:
                                code_line += name.o + f')\n'
    
    code_line += f'\n'



print(code_line)
