import Data.List

go x xs = length $ filter (==x) $ diffs $ sorted ++ [last sorted + 3]
    where diffs xs = zipWith (-) xs (0:xs)
          sorted = sort xs

main :: IO()
main = do
    contents <- readFile "input.txt"
    let input = map read $ words contents :: [Int]

    print $ go 1 input * go 3 input