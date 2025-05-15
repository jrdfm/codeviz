# AST Visualization: Field Cluster Containment Bug

## Problem Summary

When visualizing Python ASTs with Graphviz, we want list fields (like `values`, `ops`, `comparators`) to be rendered as clusters (subgraphs) that contain only the direct items of the list. If a list item is a simple node (e.g., `Eq`, `Constant`), it should appear inside the field cluster. If a list item is a `PRIMARY_CLUSTER_NODE_TYPE` (e.g., `BoolOp`, `Compare`), it should be rendered as a cluster in the parent scope, and the field cluster should only have an edge pointing to it (not contain a duplicate node).

**Observed behavior:**
- Field clusters (e.g., `<values>`, `<ops>`, `<comparators>`) are created as subgraphs in the DOT output.
- Simple nodes (like `Eq`, `Constant`) are correctly placed inside these clusters.
- When a list item is a `PRIMARY_CLUSTER_NODE_TYPE`, the actual cluster for that item (e.g., `BoolOp`, `Compare`) is rendered outside the field cluster, but a duplicate node with the same label appears inside the field cluster, leading to visual confusion and redundancy.
- The field cluster ends up empty or with a dummy node, while the real cluster is outside.

## Steps Taken So Far

1. **Initial Implementation:**
   - List fields were rendered as simple nodes (field boxes), and all items were children of these nodes.
   - This worked for clarity but did not visually group items as clusters.

2. **Attempted Field Clusters:**
   - Changed field boxes to clusters (subgraphs) for list fields.
   - Simple nodes appeared inside clusters, but when a list item was a primary cluster type, its cluster was rendered outside, and a duplicate node appeared inside the field cluster.

3. **Diagnostics:**
   - Directly defining a test node inside the field cluster worked (the node appeared inside the cluster).
   - Recursive calls for primary cluster items resulted in the real cluster being outside, and a dummy node inside.

4. **Shallow Container Logic:**
   - Tried to only create an edge from the field cluster to the primary cluster, without a node inside the field cluster.
   - The field cluster still appeared empty, and the real cluster was outside.

5. **DOT Source Inspection:**
   - Confirmed that the DOT output places simple nodes inside the field cluster subgraph, and primary clusters as subgraphs in the parent scope.
   - Edges are correctly defined from the field cluster to the primary cluster.
   - The visual output, however, is not grouping the clusters as intended.

## What to Explore Next

- **Graphviz Cluster Nesting Semantics:**
  - Investigate how Graphviz handles edges from a cluster to another cluster, and whether there is a way to visually group clusters as "shallow containers" for other clusters.
  - Explore the use of invisible anchor nodes or ports to better control edge routing and containment.

- **Graphviz Library Limitations:**
  - Check if the Python `graphviz` library has limitations or bugs with deeply nested dynamic subgraphs and node/cluster containment.
  - Try generating a minimal DOT file by hand that mimics the desired structure and see if Graphviz itself can render it as intended.

- **Alternative Visual Grouping:**
  - Consider using only edges (not clusters) to group primary clusters, or use a different visual cue (e.g., background color, border) to indicate grouping.

- **Edge Routing and Labeling:**
  - Experiment with `lhead`, `ltail`, and `group` attributes to improve edge routing between clusters and their parent field clusters.

- **Library Version:**
  - Ensure the latest version of the Python `graphviz` library is being used, and check for any known issues with cluster handling.

## Summary

The core issue is that field clusters cannot visually contain primary clusters as intended, and attempts to do so result in either empty clusters or duplicate nodes. The DOT output appears structurally correct, but Graphviz's layout engine does not render the containment as expected. Further exploration of Graphviz's cluster semantics and alternative grouping strategies is needed. 