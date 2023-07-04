from django import template
from random import shuffle
register=template.Library()

def toShuffle(value):
    a=list(value)
    b=shuffle(a)
        
    return b

    

register.filter('toShuffle',toShuffle)
#register.filter('removeChar',removeChar)  