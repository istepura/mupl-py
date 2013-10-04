<pre>
Progam -> BracketedExpression
BracketedExpression -> ( Expression )
Expression -> VAR STRING
            | INT NUMBER
            | ADD BracketedExpression BracketedExpression
            | FUN Funname STRING BracketedExpression
            | IFGRTR BracketedExpression BracketedExpression BracketedExpression BracketedExpression
            | CALL BracketedExpression BracketedExpression
            | MLET STRING BracketedExpression BracketedExpression
            | APAIR BracketedExpression BracketedExpression
            | FST BracketedExpression
            | SND BracketedExpression
            | AUNIT
            | ISAUNIT BracketedExpression
      
Funname -> STRING | FSHARP
</pre>