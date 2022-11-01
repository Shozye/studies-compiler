%{
int linecount = 0; 
int wordcount = 0;
%}
WS      [ \t]+
WORD    [^ \t\n]+

%%
^\n {linecount++;}
^{WS}
{WS}$
{WS}      {printf(" ");}
{WORD}     {printf("%s", yytext); wordcount++;}
\n { printf("\n"); linecount++;}
%%
  
int yywrap(){}
int main(){
      yylex();
      printf("%d %d\n", linecount, wordcount);
      return 0;
}