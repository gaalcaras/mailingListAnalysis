window.onload = function() {
  populateOptions();
  sortGraphs('depth', 'star_nodes');
  changeImageSize(150);
}

sortGraphs = function(crit1, crit2='depth') {
  var graphs = document.querySelectorAll('.tree'),
      graphsArr = Array.prototype.slice.call(graphs),
      grid = document.getElementById('grid'),
      elements = document.createDocumentFragment();

  document.getElementById('crit1').value = crit1;
  document.getElementById('crit2').value = crit2;

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

  if (document.getElementById('crit1-color').checked) {
    decorateGraphs(crit1);
  }
}

switchGraphDecoration = function(checked) {
  if (checked) {
    var crit1 = document.getElementById('crit1').value;
    decorateGraphs(crit1);
  } else {
    var graphs = document.querySelectorAll('.tree');

    graphs.forEach(function(graph) {
      graph.style['border-bottom'] = '2px solid white';
    })
  }
}

decorateGraphs = function(crit1) {
  var graphs = document.querySelectorAll('.tree'),
      graphsArr = Array.prototype.slice.call(graphs),
      allValues = graphsArr.map(x => x.dataset[crit1]),
      uniqueValues = [...new Set(allValues)],
      opacity = 0.1,
      step = 0.9/uniqueValues.length;

  uniqueValues.forEach(function(val) {
    var trees = document.querySelectorAll('[data-' + crit1 + '=\'' + val + '\']'),
        treesArr = Array.prototype.slice.call(trees);

    treesArr.forEach(function(tree) {
      tree.style['border-bottom'] = '2px solid rgba(0, 0, 139, ' + opacity + ')';
    });

    opacity += step;
  });
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
      elements = document.createDocumentFragment();

  options.forEach(function(option) {
    var el = document.createElement('option');
    el.value = option;
    el.innerHTML = option;

    elements.appendChild(el);
  });

  select.forEach(function(sel) {
    sel.innerHTML = null;
    sel.appendChild(elements.cloneNode(true));
  });

}

changeImageSize = function(value){
  var images = document.getElementsByTagName('img'),
      imagesArr = Array.prototype.slice.call(images);

  document.getElementById('img-size').value = value;

  imagesArr.forEach(function(img) {
    img.style.width = value + 'px';
    img.style.height = 'auto';
  })
}

changeGridMode = function(value) {
  if (value === 'list') {
    reorderGrid();
  } else {
    tableGrid();
  }
}

tableGrid = function() {
  var crit1 = document.getElementById('crit1').value,
      crit2 = document.getElementById('crit2').value,
      graphs = document.querySelectorAll('.tree'),
      graphsArr = Array.prototype.slice.call(graphs),
      var1 = [...new Set(graphsArr.map(x => x.dataset[crit1]))],
      var2 = [...new Set(graphsArr.map(x => x.dataset[crit2]))],
      // elements = document.createDocumentFragment(),
      grid = document.getElementById('grid'),
      table = document.createElement('table');

  var1.forEach(function(value) {
    var tr = document.createElement('tr'),
        trees = document.querySelectorAll('[data-' + crit1 + '=\'' + value + '\']'),
        td = document.createElement('td');

    td.innerHTML = value;
    tr.appendChild(td)

    trees.forEach(function(tree) {
      var td = document.createElement('td');
      td.appendChild(tree);
      tr.appendChild(td);
    });

    table.appendChild(tr);
  });


  grid.innerHTML = null;
  grid.appendChild(table);
}
