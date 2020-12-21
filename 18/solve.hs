import Data.Char
import Text.Parsec
import Text.Parsec.String
import Text.Parsec.Token
import Text.Parsec.Language
import Text.Parsec.Expr

import Prelude hiding (lex)

data Expr = Add Expr Expr
          | Mul Expr Expr
          | Lit Integer
    deriving (Show)

lex = makeTokenParser emptyDef
bin op cst = Infix (do { reservedOp lex op; return cst })

table  = [[bin "+" Add AssocLeft, bin "*" Mul AssocLeft]]
table' = [[bin "+" Add AssocLeft], [bin "*" Mul AssocLeft]]

lit :: Parser Expr
lit = Lit <$> integer lex

term :: Parser Expr -> Parser Expr
term p = lit <|> parens lex p

expr :: Parser Expr
expr = buildExpressionParser table $ term expr

expr' :: Parser Expr
expr' = buildExpressionParser table' $ term expr'

corr :: Either a b -> b
corr x = case x of
    Right b -> b 
    Left err -> error "Error"

eval :: Expr -> Integer
eval (Lit x) = x
eval (Add x x') = eval x + eval x'
eval (Mul x x') = eval x * eval x'

ev :: Parser Expr -> String -> Integer
ev p = eval . corr . parse p ""

go :: Parser Expr -> [String] -> Integer
go p = sum . map (ev p)

main = do
    line <- lines <$> readFile "input.txt"

    print $ go expr line
    print $ go expr' line