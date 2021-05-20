import sys

class Symbol:
    # id,scope,kind,type,signature,pline,ppos

    # id,scope,kind,type,signature,pline,ppos
    def __init__(self,id=None,scope=None,kind=None,type=None,signature=None,pline=None,ppos=None):
        if id == None and scope == None and kind == None:
            print("Symbol __init__ error: id, scope, and kind must be specified")
            sys.exit(0)
        # length >= 3
        self.name = id
        self.scope = scope
        self.kind = kind
        self.type = type
        self.signature = signature
        self.pline = pline
        self.ppos = ppos
    #end __init__

    def d_name(self):
        return self.name

    def d_scope(self):
        return self.scope

    def d_kind(self):
        return self.kind

class SymbolTab:
    def __init__(self,*argv):
        self.table = []
    
    def insertSymbol(self,id=None,scope=None,kind=None,type=None,signature=None,pline=None,ppos=None):
        s = Symbol(id=id,scope=scope,kind=kind,type=type,signature=signature,pline=pline,ppos=ppos)
        self.table.append(s)

    def showtab(self):
        for i in self.table:
            print("--------------------------------------------\n")
            print(i.name,": ",end="")
            print("scope = ",i.scope," | ",end="")
            print("kind = ",i.kind," | ",end="")
            if i.type:
                print("type = ",i.type," | ",end="")
            if i.signature:
                print("signature = ",i.signature," | ",end="")
            if i.pline:
                print("pline = ",i.pline," | ",end="")
            if i.ppos:
                print("ppos = ",i.ppos," | ",end="")
            print("\n")     

    def is_classname(self,xid):
        for i in self.table:
            if xid == i.name:
                if i.scope == "global":
                    if i.kind == "classname":
                        return i
        return None
    
    def is_constr(self,xid,scope,signature):
        for i in self.table:
            if xid == i.name:
                if i.scope == scope:
                    if i.kind == "constr":
                        if i.signature == signature:
                            return i
        return None

    def is_method(self,xid,scope,signature):
        for i in self.table:
            if i.name == xid:
                if i.scope == scope:
                    if i.kind == "method":
                        if i.signature == signature:
                            return i
        return None
    
    def is_methodname(self,xid,scope):
        for i in self.table:
            if i.name == xid:
                if i.scope == scope:
                    if i.kind == "method":
                        return i
        return None
    
    def is_attribute(self,name,scope):
        for i in self.table:
            if i.name == name:
                if i.scope == scope:
                    if i.kind == "attribute":
                        return i
        return None 

    def is_var(self,varname,scope):
        for i in self.table:
            if i.name == varname:
                if i.scope == scope:
                    if i.kind == "var":
                        return i
        return None
    
    def is_label(self,labelname,scope):
        for i in self.table:
            if i.name == labelname:
                if i.scope == scope:
                    if i.kind == "label":
                        return i
        return None
    
    def is_arg(self,varname,scope):
        for i in self.table:
            if i.name == varname:
                if i.scope == scope:
                    if i.kind == "arg":
                        return i
        return None
    
    def find(self,name,scope):
        for i in self.table:
            if i.name == name:
                if i.scope == scope:
                    print("is defined in ", i.scope,"and the type is ",i.type)
                    return i
        return None
