
data Vector a = Vector a a deriving Show

add :: Num a => Vector a -> Vector a -> Vector a
add (Vector a b) (Vector a' b') = Vector (a + a') (b + b')
    
mul :: Num a => Vector a -> a -> Vector a
mul (Vector a b) x = Vector (a * x) (b * x)

data Direction = North | East | South | West deriving (Show, Enum)

data TurnDirection = LeftTurn | RightTurn deriving Show

data Move = Forwards Int
          | InDirection Direction Int
          | TurnBy TurnDirection Int deriving Show

data Ship = Ship { direction :: Direction,
                   position :: Vector Int } deriving Show

data Ship' = Ship' { position' :: Vector Int,
                     waypoint :: Vector Int } deriving Show

sinSteps n = r `mod` 2 * (if r > 2 then -1 else 1) 
    where r = n `mod` 4
cosSteps = sinSteps . (+1)

-- rotate counterclockwise by n steps of 90 degrees
rotateSteps :: Vector Int -> Int -> Vector Int
rotateSteps (Vector x y) n = Vector (x * cosSteps n - y * sinSteps n) (x * sinSteps n + y * cosSteps n)

-- the unit vector in a given direction
unit :: Num a => Direction -> Vector a
unit North = Vector   0   1
unit East  = Vector   1   0
unit South = Vector   0 (-1)
unit West  = Vector (-1)  0

-- construct a move from a character and integer
move :: Char -> Int -> Move
move 'N' = InDirection North
move 'E' = InDirection East
move 'S' = InDirection South
move 'W' = InDirection West
move 'L' = TurnBy LeftTurn
move 'R' = TurnBy RightTurn
move 'F' = Forwards

-- get the sign of a turn direction
turnSign :: TurnDirection -> Int
turnSign LeftTurn = -1
turnSign RightTurn = 1

-- get the number of 90-degree steps to turn (anticlockwise) given a turn direction and no. degrees 
steps :: TurnDirection -> Int -> Int
steps direction degrees = turnSign direction * (degrees `div` 90)

turn :: Direction -> TurnDirection -> Int -> Direction
turn facing direction degrees = toEnum $ (fromEnum facing + steps direction degrees) `mod` 4

apply :: Ship -> Move -> Ship
apply (Ship facing position) (Forwards n) = Ship facing (add position $ mul (unit facing) n) 
apply (Ship facing position) (InDirection direction n) = Ship facing (add position $ mul (unit direction) n)
apply (Ship facing position) (TurnBy direction degrees) = Ship (turn facing direction degrees) position

apply' :: Ship' -> Move -> Ship'
apply' (Ship' position waypoint) (Forwards n) = Ship' (add position $ mul waypoint n) waypoint
apply' (Ship' position waypoint) (InDirection direction n) = Ship' position (add waypoint $ mul (unit direction) n)
apply' (Ship' position waypoint) (TurnBy direction degrees) = Ship' position (rotateSteps waypoint $ - steps direction degrees)

main :: IO()
main = do
    input <- map (\x -> move (head x) (read $ drop 1 x :: Int)) . words <$> readFile "input.txt"

    let final = foldl apply (Ship East $ Vector 0 0) input
    let final' = foldl apply' (Ship' (Vector 0 0) (Vector 10 1)) input

    let get = (\(Vector x y) -> abs x + abs y)

    print $ get (position final)
    print $ get (position' final')