

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        if len(self)==0:
            return True
        return False

    def __len__(self):
        count=0
        current=self.top
        while current is not None:
            count+=1
            current=current.next
        return count


    def push(self,value):
        new_node=Node(value)
        new_node.next=self.top
        self.top=new_node
        return None

     
    def pop(self):
        if self.isEmpty():
            return None
        x=self.top.value
        current=self.top
        self.top=current.next
        return x

    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt): # Checks if it is a valid floating number
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        try:
            k=float(txt)
            return True
        except:
            return False

    def _checkValidity(self, txt): # This function checks whether the expression whose postfix needs to be determined is valid or not. It returns if there are any unbalanced parenthese, consecutive operands, or operators
        element_txt=txt.split()
        k=0
        while k+1<len(element_txt):
            if element_txt[k] not in "+-*/^()" and self._isNumber(element_txt[k])==False:
                return False
            elif element_txt[k] in "+-*/^" and element_txt[k+1] in  "+-*/^":
                return False
            elif element_txt[-1] in "+-*/^":
                return False
            elif self._isNumber(element_txt[k])==True and self._isNumber(element_txt[k+1])==True:
                return False
            elif self.check_balanced_parentheses(element_txt)==False:
                return False
            k=k+1
        return True

    def check_balanced_parentheses(self, element_txt): # This checks whether there is a balanced parntheses or not while using a stack. It pushes the value 0 when it encounters '(' and pops when there is a ')'
        p=Stack()
        for element in element_txt:
            if element=='(':        # push 0 if the element is '('
                p.push(0)
            elif element==')':
                if p.isEmpty():
                    return False
                p.pop()            # pop 0 if the element is ')'
        if p.isEmpty():
            return True
        return False


    def extra_credit(self,txt): # This is the extra credit function that takes in consideration implicit multiplication as well. If the conditions of implicit multiplication are met, I insert a '*' in the string whose postfix needs to be calcualted.
        splits_elements=txt.split()
        p=0
        while p+1<len(splits_elements):
            if splits_elements[p]==')' and splits_elements[p+1]=='(' or self._isNumber(splits_elements[p]) and splits_elements[p+1]=='(' or splits_elements[p]==')' and self._isNumber(splits_elements[p+1]):
                splits_elements.insert(p+1,'*')
            p=p+1
        return " ".join(splits_elements)



    def _getPostfix(self, txt):
        

        # YOUR CODE STARTS HERE
        postfixStack = Stack()
        list_postfix=[]
        if self._checkValidity(txt)==False:
            return None
        extra_credit_string=self.extra_credit(txt)
        txt1=extra_credit_string.strip()
        expr_entered_elements=txt1.split(" ")
        d={'^':2, '*':1, '/':1, '+':0, '-':0,'(':-1}
        i=0
        while i<len(expr_entered_elements):
            if expr_entered_elements[i] not in "^*/+-()":       # appends an operand to the postfix list
                list_postfix.append(expr_entered_elements[i])

            elif postfixStack.isEmpty() and expr_entered_elements[i] in "^*/+-(":  # If the stack is empty and we encounter an operator, just push that to the stack
                postfixStack.push(expr_entered_elements[i])
            
            elif expr_entered_elements[i]=='(':                 # special case for  a parentheses
                postfixStack.push(expr_entered_elements[i])
            
            elif expr_entered_elements[i]==")":                # special case for  a parentheses
                current=postfixStack.top
                while postfixStack.isEmpty()==False:
                    num4=postfixStack.pop()
                    if num4 !='(':
                        list_postfix.append(num4)
                    else:
                        break
                    current=current.next
            
            elif postfixStack.isEmpty()==False and postfixStack.peek() in "^*/+-(" and expr_entered_elements[i] in "^*/+-":  # checking precedence of two operators
                
                if d[expr_entered_elements[i]]>d[postfixStack.peek()]:
                    postfixStack.push(expr_entered_elements[i])
                
                elif d[expr_entered_elements[i]]==d[postfixStack.peek()]:
                    if expr_entered_elements[i]=='^':                         # special case for the exponential function
                        postfixStack.push(expr_entered_elements[i])
                    else:
                        num8=postfixStack.pop()
                        list_postfix.append(num8)
                        postfixStack.push(expr_entered_elements[i])
                else:
                    while postfixStack.isEmpty()==False and d[expr_entered_elements[i]]<=d[postfixStack.peek()]:
                        num2=postfixStack.pop()
                        list_postfix.append(num2)
                    postfixStack.push(expr_entered_elements[i])  
            i=i+1
        
        self.postfix_add_remaining_values(postfixStack, list_postfix) # This method checks if the stack is empty or not. If it is not empty, we append all the elements from the stack to the list of postfix.


        return self.postfix_joining(list_postfix) # Joins the elements of the postfix list together. Joins operators and operands together.

    def postfix_add_remaining_values(self, postfixStack, list_postfix): # This method checks if the stack is empty or not. If it is not empty, we append all the elements from the stack to the list of postfix.
      if postfixStack.isEmpty()==False:
          while postfixStack.isEmpty()==False:
            num0=postfixStack.pop()
            list_postfix.append(num0)



    def postfix_joining(self, list_postfix): # This method checks if the element in the list is an operand or operator. If it is an operator then it can't be converted to a float, but if it is an operand it can be converted to a float.

        postfix_join_expr=[]
        for element in list_postfix:
            try:
                postfix_join_expr.append(str(float(element)))
            except:
                postfix_join_expr.append(element)
        
        return " ".join(postfix_join_expr)


    @property
    def calculate(self):
       

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression
        postfix_expr=self._getPostfix(self.getExpr)
        if postfix_expr==None: # If the postfix expression is not defined, return None
            return None
        split_postfix=postfix_expr.split(" ")
        for element in split_postfix:
            try:
                calcStack.push(float(element)) # If this statement doesn't throw an exception, then it is an operand otherwise an operator. 
            except:
                num1=calcStack.pop() # If we are in the except statement, it means we have encountered an operator, Hence, pops two values from the stack.
                num2=calcStack.pop()
                if element=='*':
                    calcStack.push(float(num2)*float(num1))
                elif element=='+':
                    calcStack.push(float(num2)+float(num1))
                elif element=='/':
                    if float(num1)==0:
                        return None
                    calcStack.push(float(num2)/float(num1))
                elif element=='-':
                    calcStack.push(float(num2)-float(num1))
                elif element=='^':
                    if float(num2)==0 and float(num1)<0:
                        return None
                    calcStack.push(float(num2)**float(num1))

        return calcStack.peek()


#=============================================== Part III ==============================================

class AdvancedCalculator:
    
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word): # Checks if we have a valif variable
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        if word[0].isalpha()==True and len(word) !=0 and word.isalnum()==True:
            return True
        return False
       

    def _replaceVariables(self, expr): # This returns a value if any of the variable values have been updated in the string.
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        list_updated_elements_list=[]
        list_elements_expr=expr.split(" ")
        j=0
        for element in list_elements_expr:
            if element not in self.states and self._isVariable(element)==False: # If we encounter an element that is not in self.states but is not a variable, then we just append the value to the list.
                list_updated_elements_list.append(element)
                j+=1
            elif element not in self.states and self._isVariable(element)==True: # If we encounter an element that is not in self.states but is a variable, then we just return None.
                return None
            else:
                list_updated_elements_list.append(str(self.states[element])) # For any other case we just append the dictionary value for the element in the list
                j+=1       
        
        if j !=0:
            return " ".join(list_updated_elements_list)
        else:
            return None

    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        d={}
        list_expr=self.expressions.split(";")
        i=0
        while i<len(list_expr)-1:
            element_expr=list_expr[i].split("=") #splits individual elements of an expression 
            index=0
            while index<len(element_expr):
                element_expr[index]=element_expr[index].strip() # Removes the extra space
                index=index+1
            if self._isVariable(element_expr[0])==False: # If the element is not a variable, return None
                self.states={}
                return None
            replace_expr=self._replaceVariables(element_expr[1])
            
            if replace_expr==None:
                self.states[element_expr[0]]=element_expr[1]
                d[list_expr[i]]=self.states.copy()
                i=i+1
            else:
                calcObj.setExpr(replace_expr)
                calc_value=calcObj.calculate
                self.states[element_expr[0]]=calc_value # update the value for self.states if the replce_expr is not None
                d[list_expr[i]]=self.states.copy()
                i=i+1
        
        # This process for finding the answer for expression in the return statement
        splitting_values_return_stat=list_expr[-1].split(" ") # Splits the values of the return expression 
        expr_without_return=' '.join(splitting_values_return_stat[1:])
        replace_for_return=self._replaceVariables(expr_without_return)
        calcObj.setExpr(replace_for_return)
        value_return_statement=calcObj.calculate 
        d['_return_']=value_return_statement
            
        return d
