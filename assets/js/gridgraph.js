window.onload = function() {
  sortGraphs('depth', 'star_nodes');
  populateOptions();
}

sortGraphs = function(crit1, crit2='depth') {
  var graphs = document.querySelectorAll('.tree'),
      graphsArr = Array.prototype.slice.call(graphs),
      grid = document.getElementById('grid'),
      elements = document.createDocumentFragment();

  graphsArr.sort(function(a, b) {
    var graph1 = a.dataset[crit1],
        graph2 = b.dataset[crit1];

    if (graph1 != graph2) {
      return graph1 - graph2
    } else {
      return a.dataset[crit2] - b.dataset[crit2]
    }
  });

  graphsArr.forEach(function(graph) {
    elements.appendChild(graph.cloneNode(true));
  });

  grid.innerHTML = null;
  grid.appendChild(elements);
}

reorderGrid = function() {
  var crit1 = document.getElementById('crit1').value,
      crit2 = document.getElementById('crit2').value;

  sortGraphs(crit1, crit2);
}

populateOptions = function() {
  var graph = document.querySelectorAll('.tree'),
      options = Object.keys(graph[0].dataset),
      select = document.querySelectorAll('.criteria'),
      selectArr = Array.prototype.slice.call(select),
      elements = document.createDocumentFragment();

  options.forEach(function(option) {
    var el = document.createElement('option');
    el.value = option;
    el.innerHTML = option;

    elements.appendChild(el);
  });

  selectArr.forEach(function(sel) {
    sel.innerHTML = null;
    sel.appendChild(elements.cloneNode(true));
  });

}

changeImageSize = function(value){
  var images = document.getElementsByTagName('img'),
      imagesArr = Array.prototype.slice.call(images);

  imagesArr.forEach(function(img) {
    img.style.width = value + 'px';
    img.style.height = value + 'px';
  })
}
