f :: Int -> Int -> Int
f s x = (s * x) `mod` 20201227

g :: Int -> Int -> Int
g s x = foldr1 (.) (replicate x (f s)) 1

g' :: Int -> Int -> Int
g' s x = snd $ until (\(x', _) -> x' == x) (\(x', i) -> (f s x', i+1)) (1, 0)

main = do
    [x, x'] <- map (read :: String -> Int) . lines <$> readFile "input.txt"
    print $ g x' $ g' 7 x