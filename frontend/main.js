import { Graphviz } from "@hpcc-js/wasm";
import svgPanZoom from "svg-pan-zoom";

// Make panZoomInstance globally accessible or scoped appropriately
// to be available for the reset button
let panZoomInstance;

async function getPythonFiles() {
  const response = await fetch('http://localhost:8000/api/list-python-files');
  return await response.json();
}

function createFilePicker(pyFiles) {
  const select = document.createElement('select');
  pyFiles.forEach(f => {
    const option = document.createElement('option');
    option.value = f;
    option.textContent = f;
    select.appendChild(option);
  });
  document.body.insertBefore(select, document.getElementById('graph'));

  select.addEventListener('change', () => {
    loadAndRenderDot(select.value);
  });

  // Load the first file by default
  if (pyFiles.length > 0) {
    loadAndRenderDot(pyFiles[0]);
    // Add reset button after the first graph is loaded
    addResetButton();
  }
}

async function loadAndRenderDot(pyFile) {
  const response = await fetch(`http://localhost:8000/api/dot/${pyFile}`);
  const dot = await response.text();
  const graphDiv = document.getElementById('graph');
  graphDiv.innerHTML = '';
  const graphviz = await Graphviz.load();
  const svg = await graphviz.layout(dot, "svg", "dot");
  graphDiv.innerHTML = svg;
  const svgElem = graphDiv.querySelector("svg");

  // Ensure the SVG element itself can fill the container
  if (svgElem) {
    svgElem.setAttribute('width', '100%');
    svgElem.setAttribute('height', '100%');
  }

  // Initialize pan/zoom
  if (panZoomInstance) {
    panZoomInstance.destroy();
  }
  panZoomInstance = svgPanZoom(svgElem, { 
    maxZoom: 5, 
    minZoom: 0.5, 
    contain: false, // Allows free dragging
    center: true    // Center the initial view
  });

  // Remove custom pan limit logic to allow free dragging
  // window.addEventListener('resize', updatePanLimits); // Comment out or remove if not needed
}

// Function to add the reset button and its event listener
function addResetButton() {
  // Check if button already exists to prevent duplicates
  if (document.getElementById('resetViewBtn')) {
    return;
  }
  const resetButton = document.createElement('button');
  resetButton.id = 'resetViewBtn';
  resetButton.textContent = 'Reset View';
  resetButton.style.position = 'absolute';
  resetButton.style.top = '10px';
  resetButton.style.right = '10px';
  resetButton.style.zIndex = '1000'; // Ensure it's on top
  document.body.appendChild(resetButton);

  resetButton.addEventListener('click', () => {
    if (panZoomInstance) {
      panZoomInstance.reset(); // Resets both pan and zoom
      panZoomInstance.center();  // Re-center the view
    }
  });
}

// On page load, fetch the file list and create the picker
getPythonFiles().then(createFilePicker);