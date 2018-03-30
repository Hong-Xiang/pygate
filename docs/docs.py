#coding:utf-8  
"""
Function to get the sum of x and y. 
Example: 
>>> mt=MyMath()  
>>> mt.add(1,2) 
3 
>>> mt.add(3,-2) 
1 
>>> mt.add(2.4,1.5) 
3.9 
"""   


class MyMath:  
    """ 
    A class with math operator 
    """  
    def add(self,x,y):  
        """ 
        Function to get the sum of x and y. 
        Example: 
        >>> mt=MyMath()  
        >>> mt.add(1,2) 
        3 
        >>> mt.add(3,-2) 
        1 
        >>> mt.add(2.4,1.5) 
        3.9 
        """  
        return x+y  