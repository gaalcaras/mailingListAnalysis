window.onload = function() {
  var graphs = new Graphs(document.querySelectorAll('.tree')),
      grid = document.getElementById('grid'),
      checkbox = document.getElementById('crit1-color');

  reorderGrid = function() {
    const crit1 = document.getElementById('crit1').value,
          crit2 = document.getElementById('crit2').value;

    graphs.var1.update(crit1);
    graphs.var2.update(crit2);

    updateGrid();
  };

  switchGraphDecoration = function(checked) {
    grid.classList.toggle('noBorder');
  };

  changeImageSize = function(value){
    graphs.imgSize.update(value);
    updateGrid();
  };

  changeGridMode = function(value){
    table = graphs.mode.update(value);
    updateGrid();
  };

  updateGrid = function() {
    const mode = document.getElementById('mode').value;
    if (mode === 'list') {
      updateElementById('grid', graphs.graphsArr);
    } else {
      updateElementById('grid', graphs.tableArr);
    }
  };

  updateElementById('crit1', generateSelect(Object.keys(graphs.vars), 'depth'));
  updateElementById('crit2', generateSelect(Object.keys(graphs.vars), 'star_nodes'));
  reorderGrid();
  changeImageSize(150);
  checkbox.checked = false;
};

function range(start, end, step = 1) {
  const len = Math.floor((end - start) / step) + 1;
  return Array(len).fill().map((_, idx) => start + (idx * step))
}

function updateElementById(id, newContent) {
  var element = document.getElementById(id),
      fragment = document.createDocumentFragment();

  newContent.forEach(function(c) {
    fragment.appendChild(c);
  });

  element.innerHTML = null;
  element.appendChild(fragment);
}

function get_graphs_vars(graphs) {
  var var_names = Object.keys(graphs[0].dataset),
      vars = [];

  var_names.forEach(name => {
    vars[name] = [...new Set(graphs.map(x => x.dataset[name]))]
  });

  return vars;
}

function Control(value, callback) {
  this.value = value;
  this.update = function(new_value) {
    if(this.value !== new_value) {
      this.value = new_value;
      callback(this.value);
    }
  };
  callback(value);
}

function Graphs(graphs) {
  this.graphsArr = Array.prototype.slice.call(graphs);
  this.tableArr = {};
  this.vars = get_graphs_vars(this.graphsArr);
  this.sort = () => {
    const mode = (typeof(this.mode) !== 'undefined') ? this.mode.value : 'list';
    if (mode === 'list') {
      this.graphsArr = this.sortList(this.graphsArr);
    } else {
      this.arrangeAsTable();
    }
  };
  this.sortList = (graphsArr) => {
    const var1 = (typeof(this.var1) !== 'undefined') ? this.var1.value : 'depth',
          var2 = (typeof(this.var2) !== 'undefined') ? this.var2.value : 'star_nodes',
          mode = (typeof(this.mode) !== 'undefined') ? this.mode.value : 'list',
          colorVar = (mode === 'list') ? var1 : var2;

    var elements = document.createDocumentFragment();

    graphsArr.sort(sortGraphs(var1, var2));
    this.addColor(colorVar);

    graphsArr.forEach(function(graph) {
      elements.appendChild(graph.cloneNode(true));
    });

    return Array.prototype.slice.call(elements.children);
  };
  this.addColor = (crit) => {
    var critValues = this.vars[crit].sort(),
        step = 0.9/critValues.length,
        seq = range(0.1, 1, step),
        opacities = {};

    critValues.forEach((key, i) => opacities[key] = seq[i]);

    this.graphsArr.forEach(function(tree) {
      tree.style['border-bottom'] = '2px solid rgba(0, 0, 139, ' + opacities[tree.dataset[crit]] + ')';
    });

  };
  this.changeSize = (value) => {
    this.graphsArr.forEach(function(tree) {
      tree.style.width = value + 'px';
      tree.style.height = value + 'px';
    });
  };
  this.arrangeAsTable = () => {
    const var1Name = (typeof(this.var1) !== 'undefined') ? this.var1.value : 'depth',
          var2Name = (typeof(this.var2) !== 'undefined') ? this.var2.value : 'star_nodes',
          var1 = this.vars[var1Name].sort(sortNumbers),
          var2 = this.vars[var2Name].sort(sortNumbers);

    var table = document.createElement('table'),
        elements = document.createDocumentFragment();

    var1.forEach((value) => {
      var tr = document.createElement('tr'),
          trees = this.graphsArr.filter(filterGraphs(var1Name, value)),
          trees = this.sortList(trees),
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

    elements.appendChild(table);
    this.tableArr = Array.prototype.slice.call(elements.children);
  };
  this.changeMode = (mode) => {
    if (mode === 'list') {
      this.sort();
    } else {
      this.arrangeAsTable();
    }
  };
  // Controls
  this.var1 = new Control('depth', this.sort);
  this.var2 = new Control('star_nodes', this.sort);
  this.mode = new Control('list', this.changeMode);
  this.imgSize = new Control(150, this.changeSize);
}

sortNumbers = function(a, b) {
  return a - b;
};

sortGraphs = function(crit1='depth', crit2='star_nodes') {
  return function(a, b) {
    var graph1 = a.dataset[crit1],
        graph2 = b.dataset[crit1];

    if (graph1 != graph2 | b === '') {
      return graph1 - graph2
    } else {
      return a.dataset[crit2] - b.dataset[crit2]
    }
  }
};

filterGraphs = function(key, value) {
  return function(element) {
    return element.dataset[key] == value;
  };
};

generateSelect = function(options, selected='depth') {
  var elements = document.createDocumentFragment();

  options.forEach(function(option) {
    var el = document.createElement('option');

    if (option === selected) {
      el.setAttribute('selected', 'selected');
    }

    el.value = option;
    el.innerHTML = option;

    elements.appendChild(el);
  });

  return Array.prototype.slice.call(elements.children);
}
