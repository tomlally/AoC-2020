import qualified Data.Set as Set
import Prelude hiding (flip)

data Dir = East | SouthEast | SouthWest | West | NorthWest | NorthEast deriving Enum

path :: String -> [Dir]
path ('e':xs)     = East:path xs
path ('s':'e':xs) = SouthEast:path xs
path ('s':'w':xs) = SouthWest:path xs
path ('w':xs)     = West:path xs
path ('n':'w':xs) = NorthWest:path xs
path ('n':'e':xs) = NorthEast:path xs
path _ = []

type Coord = (Int, Int)

delta :: Dir -> Coord
delta East      = (1, 0)
delta SouthEast = (0, 1)
delta SouthWest = (-1, 1)
delta West      = (-1, 0)
delta NorthWest = (0, -1)
delta NorthEast = (1, -1)

move :: Coord -> Dir -> Coord
move (x, y) path = let (dx, dy) = delta path in (x + dx, y + dy)

follow :: [Dir] -> Coord
follow = foldl move (0, 0)

data Tile = Black | White deriving (Eq)

flip' :: Tile -> Tile
flip' Black = White
flip' White = Black

flip :: Set.Set Coord -> Coord -> Set.Set Coord
flip xs x = set xs x $ flip' $ get xs x

set :: Set.Set Coord -> Coord -> Tile -> Set.Set Coord
set xs x Black = Set.insert x xs
set xs x White = Set.delete x xs

get :: Set.Set Coord -> Coord -> Tile
get xs x = if Set.member x xs then Black else White

count :: Set.Set Coord -> Coord -> Tile -> Int
count xs x v = length $ filter (\d -> get xs (move x d) == v) [East ..]

next :: Set.Set Coord -> Coord -> Tile
next set x = let n = count set x Black in case get set x of
    Black -> if n == 0 || n > 2 then White else Black
    White -> if n == 2 then Black else White

step :: Set.Set Coord -> Set.Set Coord
step xs = foldl (\xs' x -> set xs' x $ next xs x) Set.empty $ concatMap (\x -> x:map (move x) [East ..]) $ Set.toList xs

main = do
    paths <- map path . lines <$> readFile "input.txt"
    
    let set = foldl flip Set.empty $ map follow paths
    
    print $ Set.size set
    print $ Set.size $ foldr1 (.) (replicate 100 step) set