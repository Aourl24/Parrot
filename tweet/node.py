#from list import List

class Node:
    def __init__(self,data=None):
        self.data=data
        self.next=None
        self.prev=None
        self.left=None
        self.right=None
        
    def __str__(self):
        return str(self.data)

    def capitalize(self):
        b=[]
        a={'a':'A','b':'B','c':'C','d':'D','e':'E','f':'F','g':'G','h':'H','i':'I','j':'J','k':'K','l':'L','m':'M','n':'N','o':'O','p':'P','q':'Q','r':'R','s':'S','t':'T','u':'U','v':'V','w':'W','x':'X','y':'Y','z':'Z'}
        for data in self.data:
            try:
                c=a[data]
            except KeyError:
                c=data
            b.append(c)
           
        self.data=('').join(b)
        return self.data
            
    def count(self,arg):
        count=0
        for data in self.data:
            if data==arg:
                count+=1
        return count
    
    def index(self,arg):
        item=-1
        for data in self.data:
            item+=1
            if data==arg:
                return item
        return None
    
    def include(self,arg):
        for data in self.data:
            if arg == data:
                return True
            
        return False
        
    def prop(self):
        dic={}
        dic['next']=self.next
        dic['prev']=self.prev
        dic['left']=self.left
        dic['right']=self.next
        return dic

    #def transform(self,to='string',value=None):
#        available=['string','dict','list','set','tuple']
#        if to not in available:
#            print('Unable to Transform')
#            return None
#        if to=='dict':
#            if value==None:
#                print('Value is required to transform a dictionary')
#                return None
#            a={}
#            g=List()
#            c=g.append(self.data)
#            b=g.loop(value)
#            print(b)
#            for data in b:
#                
#                for i in data:
#                    a[i]=data
#            self.data=a
#            return self.data
#            
#        elif to=='list':
#            a=[]
#            for data in self.data:
#                a.append(data)
#            self.data=a
#            return self.data
#        else:
#            pass
               
n1=Node('hello')
n2=Node('Hw far')
n3=Node('I like You for Everything')
n3.next=n2
#print(n1.prop())
#n2.capitalize()
#n3.capitalize()
#g=n3.count('E')
#l=n3.index('L')
#p=n3.include('X')
#n1.transform('dict','good')
#print(n3)
#print(g)
#print(l)
#print(p)
#print(n1)