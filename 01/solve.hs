import System.IO

main :: IO()
main = do
    file <- openFile "input.txt" ReadMode
    content <- hGetContents file
    let nums = map read $ words content :: [Int]

    print $ product . head $ filter (\x -> sum x == 2020) [[x, y] | x <- nums, y <- nums]
    print $ product . head $ filter (\x -> sum x == 2020) [[x, y, z] | x <- nums, y <- nums, z <- nums]