## Frontend Dependencies

The frontend now uses [@hpcc-js/wasm](https://www.npmjs.com/package/@hpcc-js/wasm) for client-side Graphviz (DOT-to-SVG) rendering, and [svg-pan-zoom](https://www.npmjs.com/package/svg-pan-zoom) for interactive pan/zoom.

Install the required npm packages:

```bash
npm install @hpcc-js/wasm svg-pan-zoom
```

- **@hpcc-js/wasm**: Runs Graphviz in the browser via WebAssembly, allowing you to render DOT to SVG client-side.
- **svg-pan-zoom**: Enables interactive panning and zooming of the SVG output.

**Note:** Viz.js is no longer required for the frontend. 