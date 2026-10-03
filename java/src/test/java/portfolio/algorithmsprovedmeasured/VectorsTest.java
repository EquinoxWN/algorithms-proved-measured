package portfolio.algorithmsprovedmeasured;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/** Runs every shared vector in spec/vectors against the Java implementations. */
class VectorsTest {
    private static final Path VECTORS = Path.of("..", "spec", "vectors");
    private static final ObjectMapper JSON = new ObjectMapper();

    @TestFactory
    Stream<DynamicTest> sharedVectors() throws IOException {
        List<DynamicTest> tests = new ArrayList<>();
        for (String name : List.of("lower_bound", "merge_sort", "dijkstra", "edit_distance", "find_all")) {
            JsonNode doc = JSON.readTree(Files.readString(VECTORS.resolve(name + ".json")));
            for (JsonNode c : doc.get("cases")) {
                tests.add(DynamicTest.dynamicTest(name + ": " + c.get("name").asText(),
                        () -> assertEquals(c.get("expect"), run(name, c.get("input")))));
            }
        }
        return tests.stream();
    }

    /** Calls one implementation and converts its result to JSON for comparison. */
    private static JsonNode run(String name, JsonNode in) throws IOException {
        Object result = switch (name) {
            case "lower_bound" -> Search.lowerBound(ints(in.get("items")), in.get("target").asInt());
            case "merge_sort" -> Sorting.mergeSort(ints(in.get("items")));
            case "dijkstra" -> Graphs.dijkstra(in.get("n").asInt(), edges(in.get("edges")), in.get("source").asInt());
            case "edit_distance" -> DynamicProgramming.editDistance(in.get("a").asText(), in.get("b").asText());
            case "find_all" -> Strings.findAll(in.get("text").asText(), in.get("pattern").asText());
            default -> throw new IllegalArgumentException(name);
        };
        return JSON.readTree(JSON.writeValueAsString(result));
    }

    /** JSON array to int[]. */
    private static int[] ints(JsonNode node) {
        int[] out = new int[node.size()];
        for (int i = 0; i < out.length; i++) {
            out[i] = node.get(i).asInt();
        }
        return out;
    }

    /** JSON [[u, v, w], ...] to int[][]. */
    private static int[][] edges(JsonNode node) {
        int[][] out = new int[node.size()][];
        for (int i = 0; i < out.length; i++) {
            out[i] = ints(node.get(i));
        }
        return out;
    }
}
