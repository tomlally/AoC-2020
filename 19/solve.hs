import Data.List.Split
import qualified Data.Map as Map

type Rules = Map.Map Int Rule
data Rule = Chr Char | Seq [Int] | Any [Rule] deriving Show

without :: Eq a => a -> [a] -> [a]
without x  []                 = []
without x' (x:xs) | x == x'   =   without x' xs
                  | otherwise = x:without x' xs

isChr :: String -> Bool
isChr xs = head xs == '\"'

ruleChr :: String -> Rule
ruleChr xs = Chr $ xs !! 1

ruleSeq :: String -> Rule
ruleSeq xs = Seq $ map read $ words xs

isAny :: String -> Bool
isAny = elem '|'

ruleAny :: String -> Rule
ruleAny xs = Any $ map ruleSeq $ splitOn "|" xs

rule' :: String -> Rule
rule' xs | isChr  xs = ruleChr xs
         | isAny  xs = ruleAny xs
         | otherwise = ruleSeq xs

rule :: String -> (Int, Rule)
rule xs = let [n, xs'] = splitOn ": " xs in (read n, rule' xs')

rules :: [String] -> Rules
rules xs = Map.fromList $ map rule xs

match' :: Rules -> Rule -> String -> [String]
match'  _ (Chr x) (x':xs) | x == x' = [xs]
                          | otherwise = []
match'  _ (Seq [])     xs = [xs]
match' rs (Seq (i:is)) xs = concatMap (match' rs (Seq is)) $ match' rs (rs Map.! i) xs
match' rs (Any rs')    xs = concatMap (\r -> match' rs r xs) rs'
match' _ _ xs = []

match :: Rules -> Int -> String -> Int
match rs i str = length $ filter (=="") $ match' rs (rs Map.! i) str

p2 :: Rules -> Rules
p2 rs = Map.insert 11 (Any [Seq [42, 31], Seq [42, 11, 31]]) $ Map.insert 8 (Any [Seq [42], Seq [42, 8]]) rs

go :: Rules -> [String] -> Int
go rs xs = sum $ map (match rs 0) xs

main = do
    content <- readFile "input.txt"
    let (ruleStrs, inputStrs) = (lines ruleStr, lines inputStr) where [ruleStr, inputStr] = splitOn "\n\n" content
    
    let rs = rules ruleStrs
    let rs' = p2 rs
    
    print $ go rs inputStrs
    print $ go rs' inputStrs