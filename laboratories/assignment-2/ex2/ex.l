%{
#include<stdbool.h>
bool inside_string = false; 
bool inside_comment = false;
int border_type = 0;
%}
%%
\"\"\" {
    if (!inside_comment) {
        printf("%s", yytext);
        if(inside_string && border_type == 0){
            inside_string = false;
        } else if (!inside_string){
            border_type = 0;
            inside_string = true;
        }
    }
}
\" {
    if (!inside_comment) {
        printf("%s", yytext);
        if(inside_string && border_type == 1){
            inside_string = false;
        } else if (!inside_string){
            border_type = 1;
            inside_string = true;
        }
    }
}
\' {
    if (!inside_comment) {
        printf("%s", yytext);
        if(inside_string && border_type == 2){
            inside_string = false;
        } else if (!inside_string){
            border_type = 2;
            inside_string = true;
        }
    }
}
\# {if(inside_string){
    printf("%s", yytext);
} else {
    inside_comment = true;
}}

. {if(!inside_comment){
    printf("%s", yytext);
}}

\n {
    printf("\n");
    inside_comment = false;
}

%%
  
int yywrap(){}
int main(){
      yylex();
      return 0;
}