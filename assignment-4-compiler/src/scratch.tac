P_decrement | 
            | PARAM  a
            | PARAM  $ret
            | a := a - 1
            | RETURN     
P_increment | 
            | PARAM  a   
            | PARAM  $ret
            | a := a + 1
            | RETURN     
P_mul       | 
            | PARAM  a   
            | PARAM  b   
            | PARAM  p   
            | PARAM  $ret
            | LOCAL  a_copy
            | a_copy := a    
            | p := 0    
E_WHILE_0   | IF a_copy = 0 GOTO E_ENDWHILE_0
            | p := p + b     
            | PUSH   a_copy
            | PUSH   E_RETURN_0
            | CALL   P_increment
E_RETURN_0  | 
            | GOTO E_WHILE_0
E_ENDWHILE_0 | 
             | RETURN            
P_PROG       | 
             | LOCAL  a          
             | LOCAL  b          
             | LOCAL  p          
             | READ   a          
             | READ   b          
             | PUSH   a          
             | PUSH   b          
             | PUSH   p          
             | PUSH   E_RETURN_1 
             | CALL   P_mul      
E_RETURN_1   | 
             | WRITE  p          
             | RETURN            
