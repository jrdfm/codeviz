# Code2Viz Graphviz Roadmap (4 Weeks)

## Week 1: Core AST-to-DOT Pipeline
```bash
Milestone: Basic AST → SVG Conversion
```
### Objectives
- [x] Python AST Parser
  - Handle function/class definitions
  - Capture line numbers
  - Simple value extraction
- [x] DOT Generator
  - Node/edge creation
  - Basic styling attributes
  - Cluster subgraphs
- [x] CLI Interface
  - File input handling
  - Graphviz rendering
  - Output file management

```python
# Sample DOT output target
digraph ast {
  node [shape=record fontname="Fira Code"]
  "FunctionDef_factorial_1" [label="{FunctionDef|factorial|Line 1}"]
  "arguments_1" [label="{arguments||Line 1}"]
  "FunctionDef_factorial_1" -> "arguments_1"
}
```

## Week 2: Enhanced Visualization & Web Preview
```bash
Milestone: Interactive Web Viewer
```
### Objectives
- [ ] Web Renderer
  - Integrate Viz.js for browser-based SVG rendering.
  - Add pan/zoom controls for interactive navigation.
  - Implement node tooltips for additional information.
- [ ] DOT Improvements
  - Implement color coding by node type for better visual distinction.
  - Add HTML-like labels for enhanced readability.
  - Include edge labels to clarify relationships between nodes.
- [ ] Development Workflow
  - Set up auto-reload on changes for a seamless development experience.
  - Establish a live server setup for real-time testing.
  - Ensure cross-platform compatibility for all features.

### Detailed Tasks
1. **Web Renderer Integration**:
   - Research and select the appropriate version of Viz.js.
   - Create a basic HTML template for the web viewer.
   - Implement the rendering logic to convert DOT to SVG.
   - Add event listeners for pan and zoom functionality.

2. **DOT Enhancements**:
   - Define a color scheme for different node types.
   - Modify the DOT generation logic to include HTML-like labels.
   - Test the rendering with various node types to ensure consistency.

3. **Development Environment**:
   - Set up a local development server using a tool like `live-server`.
   - Configure the server to automatically reload on file changes.
   - Test the setup on different operating systems to ensure compatibility.

### Expected Outcomes
- A fully functional web viewer that renders AST visualizations with interactive features.
- Enhanced DOT output with improved styling and readability.
- A streamlined development workflow that supports rapid iteration and testing.

### Step-by-Step Plan
1. **Step 1: Web Renderer Integration**
   - Research and select the latest stable version of Viz.js.
   - Create a basic HTML structure for the web viewer.
   - Implement JavaScript code to convert DOT to SVG using Viz.js.
   - Integrate a library for pan and zoom functionality.

2. **Step 2: DOT Enhancements**
   - Define a color scheme for different node types.
   - Update the DOT generation logic to apply colors and HTML-like labels.
   - Test the rendering with various node types to ensure consistency.

3. **Step 3: Development Environment**
   - Set up a local development server using `live-server`.
   - Configure the server to automatically reload on file changes.
   - Test the setup on different operating systems to ensure compatibility.

4. **Step 4: Documentation and Testing**
   - Document the implementation of the web viewer.
   - Conduct user testing to gather feedback and make necessary adjustments.

## Week 3: Multi-Language Support & Optimizations
```bash
Milestone: JavaScript Support + Performance
```
### Objectives
- [ ] JavaScript Parser
  - Babel parser integration
  - ES module analysis
- [ ] Performance
  - AST node filtering
  - Level-based rendering
  - DOT simplification
- [ ] Enhanced CLI
  - Batch processing
  - Directory scanning
  - Format conversion

```python
# Performance optimization
def simplify_dot(dot):
    return dot.unflatten(stagger=3).pipe(engine='sfdp')
```

## Week 4: Distribution & Advanced Features
```bash
Milestone: v1.0 Release
```
### Objectives
- [ ] Packaging
  - PIP package (Python core)
  - NPM package (Web viewer)
  - Docker image
- [ ] IDE Integration
  - VSCode extension skeleton
  - Context menu integration
- [ ] Documentation
  - User guide
  - API reference
  - Troubleshooting

## Technology Stack
| Component       | Technology       | Purpose                      |
|-----------------|------------------|------------------------------|
| Core Parser     | Python ast       | AST extraction               |
| DOT Generation  | graphviz-py      | Graphviz integration         |
| Web Renderer    | Viz.js           | Browser-based SVG rendering  |
| CLI Framework   | Click            | Command-line interface       |
| Packaging       | setuptools       | Python distribution          |
| Testing         | pytest           | Test framework               |

## Risk Mitigation
1. **Complex ASTs**: Limit depth with `--max-depth` CLI option
2. **Browser Performance**: Implement virtual scrolling
3. **Graphviz Errors**: Add validation layer before rendering
4. **Cross-Platform Issues**: Use Docker for consistent env

## Success Metrics
1. 90% Python syntax coverage
2. <2s render time for 500-node AST
3. 95% test coverage for core modules
4. Support 3 output formats (SVG/PNG/DOT)

## Weekly Checkpoints
- **Week 1**: `python code2viz.py sample.py -o ast.svg`
- **Week 2**: Live web viewer with zoom
- **Week 3**: `code2viz js sample.js -f png`
- **Week 4**: `pip install code2viz` working

## Stretch Goals
- C/C++ support via Clang AST
- Visual Studio integration
- PDF export with LaTeX
- Interactive node editing

# Phase Implementation Guide

1. **Day 1-3**: Python AST → DOT with basic nodes
2. **Day 4-5**: CLI with Graphviz rendering
3. **Day 6-7**: Web viewer prototype
4. **Day 8-10**: Style customization
5. **Day 11-14**: JavaScript support
6. **Day 15-20**: Performance optimizations
7. **Day 21-28**: Packaging & documentation 