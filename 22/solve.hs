import Data.List.Split
import qualified Data.Set as Set

type State = ([Int], [Int])

adv :: State -> State
adv (x:xs, y:ys) | x > y = (xs ++ [x,y], ys)
                 | y > x = (xs, ys ++ [y,x])
adv state@(xs, []) = state
adv state@([], ys) = state

score :: [Int] -> Int 
score xs = sum $ zipWith (*) (reverse xs) [1..]

result :: State -> Int
result (xs, []) = score xs
result ([], ys) = score ys

rc :: Set.Set State -> State -> State
rc _ state@(xs, []) = state
rc _ state@([], ys) = state
rc prev state@(xs, ys)
  | Set.member state prev = (xs, [])
  | otherwise = rc' (Set.insert state prev) state

rc' :: Set.Set State -> State -> State
rc' prev state@(x:xs, y:ys)
  | length xs >= x && length ys >= y =
      case rc prev (take x xs, take y ys) of
        (_, []) -> rc prev (xs ++ [x,y], ys)
        ([], _) -> rc prev (xs, ys ++ [y,x])
  | otherwise = rc prev $ adv state

p1 :: State -> State
p1 = until (\(xs, ys) -> null xs || null ys) adv

p2 :: State -> State
p2 = rc Set.empty

main = do
    content <- readFile "input.txt"
    let state = (p1, p2) where [p1, p2] = map (map (read :: String -> Int) . drop 1 . lines) $ splitOn "\n\n" content

    print $ result $ p1 state
    print $ result $ p2 state
