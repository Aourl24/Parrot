from .node import Node
       
class Cell(Node):
    def __init__(self,data):
        self.data=data
        self.datalist=[]
    
    def div(self,arg=None):
        fake=[]
        if arg=='word':
            b=self.data.split()
            fake=b
        if arg==None:
            return self.data
        return fake
        
    def split(self,arg=None):
        if arg==None:
            getDiv=self.div()
        else:
            getDiv=self.div('word')
        for i in getDiv:
            b=Node(i)
            self.datalist.append(b)
            
        return self.datalist

    def most(self, x='letter', many=0):
        res=[]
        if  many == 0:
            pos=[]
        else:
            pos={}
            
        words=None
        if x=='letter':
            words=self.data
        elif x =='word':
            words=self.data.split()
        else:
            raise UnknownArgument
           
        for i in words:
            if i==' ':
                pass
            else:
                v=words.count(i)
                res.append(v)
                
                if  many ==0:
                    pos.append(i)
                else:
                    pos[v]=i
        

        #answer=pos[gg]
        #print(res)
        if many == 0:
            mm=max(res)
            gg=res.index(mm)
            answer=pos[gg]
        else:
            fk=[]
            mn=res.sort()
            print(res)
            for k in res:
                fk.append(pos[k])
            answer=fk
            
        return answer
            
                
                                
    def __str__(self):
        return self.data
 
class UnknownArgument(Exception):
    pass    
