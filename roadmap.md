# Code2Viz Graphviz Roadmap (4 Weeks)

## Week 1: Core AST-to-DOT Pipeline
```bash
Milestone: Basic AST → SVG Conversion
```
### Objectives
- [ ] Python AST Parser
  - Handle function/class definitions
  - Capture line numbers
  - Simple value extraction
- [ ] DOT Generator
  - Node/edge creation
  - Basic styling attributes
  - Cluster subgraphs
- [ ] CLI Interface
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
  - Viz.js integration
  - Pan/Zoom controls
  - Node tooltips
- [ ] DOT Improvements
  - Color coding by node type
  - HTML-like labels
  - Edge labels
- [ ] Development Workflow
  - Auto-reload on changes
  - Live server setup
  - Cross-platform testing

```javascript
// Web viewer features
const viz = new Viz();
viz.renderSVGElement(dotText).then(svg => {
  svgPanZoom(svg, {
    maxZoom: 5,
    minZoom: 0.5
  });
  document.getElementById('graph').appendChild(svg);
});
```

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

Would you like to adjust any priorities or dive deeper into specific components?