import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.stream.Collectors;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;

public class Solve {

    static final int TILE_SIZE = 10;
    
    static enum Edge {
        Top(0),
        Right(1),
        Bottom(2),
        Left(3);

        public Edge opposite() {
            switch (this) {
                case Top: return Edge.Bottom;
                case Right: return Edge.Left;
                case Bottom: return Edge.Top;
                case Left: return Edge.Right;
                default: return null;
            }
        }

        public Coord offset() {
            switch (this) {
                case Top: return new Coord(0, -1);
                case Right: return new Coord(1, 0);
                case Bottom: return new Coord(0, 1);
                case Left: return new Coord(-1, 0);
                default: return null;
            }
        }

        public int index() {
            return m_Value;
        }

        int m_Value;
        
        private Edge(int value) {
            m_Value = value;
        }
    };

    // possible transformations
    static enum Transform {
        Rotate,
        FlipX,
        FlipY
    };

    // (hopefully) all permutations given the set of transforms
    static final Transform[][] allTransformPerms = {
        { }, // none
       
        { Transform.FlipX },    // (rotate 0,) flip x
        { Transform.FlipY },    // (rotate 0,) flip y
        
        { Transform.Rotate }, // rotate 90
        { Transform.Rotate, Transform.Rotate }, // rotate 180
        { Transform.Rotate, Transform.Rotate, Transform.Rotate }, // rotate 270
       
        { Transform.Rotate, Transform.FlipX }, // rotate 90, flip x
        //{ Transform.Rotate, Transform.Rotate, Transform.FlipX }, // rotate 180, flip x
        { Transform.Rotate, Transform.Rotate, Transform.Rotate, Transform.FlipX }, // rotate 270, flip x
        
        { Transform.Rotate, Transform.FlipY }, // rotate 90, flip y
        { Transform.Rotate, Transform.Rotate, Transform.FlipY }, // rotate 180, flip y
        { Transform.Rotate, Transform.Rotate, Transform.Rotate, Transform.FlipY }, // rotate 270, flip y
    };
    
    // simple coordinate class
    static class Coord {
        public int x, y;

        public Coord(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public Coord add(Coord other) {
            return new Coord(this.x + other.x, this.y + other.y);
        }

        @Override
        public boolean equals(Object object) {
            if (this == object) return true;
            Coord other = (Coord)object;
            return this.x == other.x && this.y == other.y;
        }

        @Override
        public int hashCode() {
            return this.x ^ this.y;
        }
    }

    static final Coord[][] EDGE_COORDS = {
        { new Coord(0, 0), new Coord(1, 0), new Coord(2, 0), new Coord(3, 0), new Coord(4, 0), new Coord(5, 0), new Coord(6, 0), new Coord(7, 0), new Coord(8, 0), new Coord(9, 0) },
        { new Coord(9, 0), new Coord(9, 1), new Coord(9, 2), new Coord(9, 3), new Coord(9, 4), new Coord(9, 5), new Coord(9, 6), new Coord(9, 7), new Coord(9, 8), new Coord(9, 9) },
        { new Coord(9, 9), new Coord(8, 9), new Coord(7, 9), new Coord(6, 9), new Coord(5, 9), new Coord(4, 9), new Coord(3, 9), new Coord(2, 9), new Coord(1, 9), new Coord(0, 9) },
        { new Coord(0, 9), new Coord(0, 8), new Coord(0, 7), new Coord(0, 6), new Coord(0, 5), new Coord(0, 4), new Coord(0, 3), new Coord(0, 2), new Coord(0, 1), new Coord(0, 0) }
    };
    
    static class TransformationApplicator {
        int size;
        
        public TransformationApplicator(int size) {
            this.size = size;
        }
        
        // NB: this is inverse in a way - corresponds to transforming space below coord
        public Coord applyTransform(Transform transform, Coord coord) {
            switch (transform) {
                case FlipX: return new Coord((this.size-1)-coord.x, coord.y);
                case FlipY: return new Coord(coord.x, (this.size-1)-coord.y);
                case Rotate: return new Coord(coord.y, (this.size-1)-coord.x);
                default: return null;
            }
        }

        public Coord applyTransform(Transform[] transforms, Coord coord) {
            if (transforms != null) for (Transform transform : transforms) coord = this.applyTransform(transform, coord);
            return coord;
        }
    }

    static Boolean toValue(char c) {
        return c == '#';
    }

    static char fromValue(Boolean v) {
        return v ? '#' : '.';
    }

    static class Tile {
        static final TransformationApplicator TRANSFORMER = new TransformationApplicator(TILE_SIZE); 

        final boolean[][] content = new boolean[10][10];
        
        public Tile(String input) {
            String[] lines = input.split("\n");
            for (int y = 0; y < 10; ++y) for (int x = 0; x < 10; ++x) this.content[y][x] = toValue(lines[y+1].charAt(x));
        }
        
        public boolean get(int x, int y) {
            return this.content[y][x];
        }
        
        public boolean get(Coord coord) {
            return get(coord.x, coord.y);
        }

        public boolean get(int x, int y, Transform[] transform) {
            return this.get(TRANSFORMER.applyTransform(transform, new Coord(x, y)));
        }

        public boolean get(Coord coord, Transform[] transform) {
            return this.get(TRANSFORMER.applyTransform(transform, coord));
        }
    }

    public static class TransformedTile {
        final Integer m_Id;
        final Transform[] transform;

        public TransformedTile(Integer id, Transform[] transform) {
            this.m_Id = id;
            this.transform = transform;
        }
    }
    
    // tile id -> tile data
    Map<Integer, Tile> m_TileMap = new HashMap<>();

    public Solve(String input)
    {
        String[] inputs = input.split("\n\n");
        for (String str : inputs) {
            Integer id = Integer.parseInt(str.substring(5, 5+4));
            this.m_TileMap.put(id, new Tile(str));
        }
    }
    
    // check that values at two coordinates cA, and cB are the same in two tiles, with two different transforms applied 
    boolean check(Tile tileA, Transform[] transformA, Coord cA, Tile tileB, Transform[] transformB, Coord cB) {
        return tileA.get(cA, transformA) == tileB.get(cB, transformB);
    }

    boolean checkEdges(Integer tileA, Transform[] transformA, Edge edgeA, Integer tileB, Transform[] transformB, Edge edgeB) {
        for (int i = 0; i < 10; ++i) {
            if (!check(m_TileMap.get(tileA), transformA, EDGE_COORDS[edgeA.index()][i], m_TileMap.get(tileB), transformB, EDGE_COORDS[edgeB.index()][9-i])) return false;
        }
        return true;
    }

    boolean checkEdges(TransformedTile tileA, Edge edgeA, TransformedTile tileB, Edge edgeB) {
        return checkEdges(tileA.m_Id, tileA.transform, edgeA, tileB.m_Id, tileB.transform, edgeB);
    }
        
    ArrayList<TransformedTile> potentialNeighbours(Integer tile, Transform[] tileTransform, Edge edge) {
        ArrayList<TransformedTile> results = new ArrayList<>();

        for (var other : m_TileMap.keySet()) {
            if (other == tile || m_IsPlaced.contains(other)) continue;

            for (Transform[] transform : allTransformPerms) {    
                if (checkEdges(tile, tileTransform, edge, other, transform, edge.opposite())) {
                    results.add(new TransformedTile(other, transform));
                }
            }
        }

        return results;
    }
    
    public ArrayList<TransformedTile> potentialNeighbours(TransformedTile tile, Edge edge) {
        return potentialNeighbours(tile.m_Id, tile.transform, edge);
    }

    // count number of edges with at least 1 valid neighbour
    int count(Integer tile) {
        int sum = 0;
        for (Edge edge : Edge.values()) if (potentialNeighbours(tile, null, edge).size() > 0) sum += 1;
        return sum;
    };
    
    // solve 1 (cheaty method)
    public long part1() {
        long prod = 1;
        for (var entry : m_TileMap.entrySet()) if (count(entry.getKey()) == 2) prod *= entry.getKey();  // if a tile exactly edges with potential neighbours 2 then it's a corner
        return prod;
    }

    // part 2
    
    Map<Coord, TransformedTile> m_Placement = new HashMap<>(); // map of coordinates -> tile id + transformation
    Set<Integer> m_IsPlaced = new HashSet<>(); // set of mapped tile ids

    // place a transformed tile at coordinate coord. Only call if certain that the tile goes at that coord.
    void place(Coord coord, TransformedTile tile) {
        m_IsPlaced.add(tile.m_Id);
        m_Placement.put(coord, tile);
    }

    // check that a tile can be placed at coord without conflicting with existing tiles.
    boolean canPlace(Coord coord, TransformedTile tile) {
        for (Edge edge : Edge.values()) {
            Coord adjCoord = coord.add(edge.offset());
            
            if (m_Placement.containsKey(adjCoord)) {
                TransformedTile adj = m_Placement.get(adjCoord);
                if (!checkEdges(tile, edge, adj, edge.opposite())) return false;
            }
        }
        return true;
    }

    static class Placement {
        final Coord coord;
        final TransformedTile tile;

        public Placement(Coord coord, TransformedTile tile) {
            this.coord = coord;
            this.tile = tile;
        }
    };

    Placement findPlacement() {
        for (var entry : m_Placement.entrySet()) {
            for (Edge edge : Edge.values()) {
                Coord adjCoord = entry.getKey().add(edge.offset());
                
                if (!m_Placement.containsKey(adjCoord)) {
                    var potentials = potentialNeighbours(entry.getValue(), edge);

                    if (potentials.size() >= 1) {   // ...
                        var potential = potentials.get(0);
                        //System.out.println(entry.getValue().m_Id + " -> " + edge + " -> " + n.m_Id);
                        if (canPlace(adjCoord, potential)) return new Placement(adjCoord, potential);
                    }
                }
            }
        }
        return null;
    }

    void placeTiles() {
 
        int an_id = m_TileMap.entrySet().iterator().next().getKey();
        place(new Coord(0, 0), new TransformedTile(an_id, null));

        // while not every tile has been placed
        while (m_Placement.size() < m_TileMap.size()) {
            Placement placement = findPlacement();
            if (placement != null) place(placement.coord, placement.tile);
            //else break; ?
        }
    }

    Coord getMin() {
        Coord min = new Coord(Integer.MAX_VALUE, Integer.MAX_VALUE);
        for (Coord coord : m_Placement.keySet()) if (coord.x < min.x || coord.y < min.y) min = coord;
        return min;
    }

    Coord getMax() {
        Coord max = new Coord(Integer.MIN_VALUE, Integer.MIN_VALUE);
        for (Coord coord : m_Placement.keySet()) if (coord.x > max.x || coord.y > max.y) max = coord;
        return max;
    }

    boolean transformedTileGet(TransformedTile tile, int x, int y) {
        return this.m_TileMap.get(tile.m_Id).get(x, y, tile.transform);
    }

    boolean[][] stitch() {
        Coord min = getMin();
        Coord max = getMax();

        int w = max.x+1 - min.x;
        int h = max.y+1 - min.y;

        boolean[][] result = new boolean[w*8][h*8];

        for (int y = min.y; y < max.y+1; y++) {
            for (int x = min.x; x < max.x+1; x++) {
                Coord coord = new Coord(x, y);
                TransformedTile tile = m_Placement.get(coord);
                
                for (int yi = 0; yi < 8; ++yi)
                for (int xi = 0; xi < 8; ++xi)
                result[(Math.abs(min.y)+y)*8+yi][(Math.abs(min.x)+x)*8+xi] = transformedTileGet(tile, xi+1, /*9-*/(yi+1));  // hacky y-coord inversion
            }
        }

        return result;
    }

    static int countPattern(Transform[] transform, boolean[][] source, boolean[][] pattern) {
        TransformationApplicator transformer = new TransformationApplicator(source.length);

        int sum = 0;
        for (int y = 0; y < source.length - pattern.length; ++y) {
            for (int x = 0; x < source[0].length - pattern[0].length; ++x) {
                
                boolean failed = false;
                for (int dy = 0; dy < pattern.length && !failed; ++dy) {
                    for (int dx = 0; dx < pattern[0].length && !failed; ++dx) {                        
                        Coord coord = transformer.applyTransform(transform, new Coord(x + dx, y + dy));

                        if (coord.y < 0 || coord.y >= source.length || coord.x < 0 || coord.x >= source[0].length) failed = true;
                        else if (pattern[dy][dx]) if (!source[coord.y][coord.x]) failed = true;
                    }
                }
                
                if (!failed) sum++;
            }
        }
        return sum;
    }

    static int sum(boolean[][] source) {
        int sum = 0;
        for (int y = 0; y < source.length; ++y) for (int x = 0; x < source[y].length; ++x) if (source[y][x]) ++sum;
        return sum;
    }

    static final String FISH =
        "                  # " + "\n" +
        "#    ##    ##    ###" + "\n" +
        " #  #  #  #  #  #   ";
    static final boolean[][] FISH_BOOLEAN = readPattern(FISH);

    static boolean[][] readPattern(String pattern) {
        String[] lines = pattern.split("\n");
        boolean[][] results = new boolean[lines.length][];
        for (int i = 0; i < lines.length; ++i) {
            results[i] = new boolean[lines[i].length()];
            for (int j = 0; j < lines[i].length(); ++j) results[i][j] = toValue(lines[i].charAt(j));
        }
        return results;
    }

    int part2() {
        this.placeTiles();
        boolean[][] stitched = stitch();

        int fishsz = sum(FISH_BOOLEAN);
        int hashes = sum(stitched);
        
        for (Transform[] transform : allTransformPerms) {
            int fishies = countPattern(transform, stitched, FISH_BOOLEAN);
            if (fishies != 0) return hashes - (fishies * fishsz);
        }
        return -1;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader buf = new BufferedReader(new FileReader(args.length >= 1 ? args[0] : "input.txt"));
        String input = buf.lines().collect(Collectors.joining("\n"));
        buf.close();
        
        Solve solve = new Solve(input);
        System.out.println(solve.part1());
        System.out.println(solve.part2());
    }
}
