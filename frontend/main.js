import svgPanZoom from 'svg-pan-zoom';

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
  }
}

async function loadAndRenderDot(pyFile) {
  const response = await fetch(`http://localhost:8000/api/dot/${pyFile}`);
  const dot = await response.text();
  const viz = new Viz();
  const graphDiv = document.getElementById('graph');
  graphDiv.innerHTML = '';
  viz.renderSVGElement(dot).then(svg => {
    // Add a large transparent rect to the SVG background for infinite panning
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', -10000);
    rect.setAttribute('y', -10000);
    rect.setAttribute('width', 20000);
    rect.setAttribute('height', 20000);
    rect.setAttribute('fill', 'transparent');
    svg.insertBefore(rect, svg.firstChild);

    graphDiv.appendChild(svg);
    const panZoom = svgPanZoom(svg, { maxZoom: 5, minZoom: 0.5, contain: false, center: true });
    panZoom.fit();
    panZoom.center();
  });
}

// On page load, fetch the file list and create the picker
getPythonFiles().then(createFilePicker);