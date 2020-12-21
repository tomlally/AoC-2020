import System.IO

p1 n xs = fst . head . filter (not . uncurry valid) $ zip (drop n xs) (drop n $ map (\i -> take n . reverse $ take i xs) [0..length xs])
    where valid x xs = x `elem` [x + x' | x <- xs, x' <- xs]

p2 x xs = let cl = head . filter (\xs -> sum xs == x) $ [drop j $ take i xs | i <- [2..length xs], j <- [0..i-2]] in minimum cl + maximum cl

main :: IO()
main = do
    file <- openFile "input.txt" ReadMode
    contents <- hGetContents file
    let list = map read $ words contents :: [Int]
    
    let a = p1 25 list
    let b = p2 a list
    
    print a
    print b
    