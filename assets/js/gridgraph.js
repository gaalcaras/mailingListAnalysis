window.onload = function() {
  var graphs = new Graphs(document.querySelectorAll('.tree')),
      vars = Object.keys(graphs.vars),
      grid = document.getElementById('grid');

  reorderGrid = function() {
    const crit1 = document.getElementById('crit1').value,
          crit2 = document.getElementById('crit2').value;

    graphs.var1.update(crit1);
    graphs.var2.update(crit2);

    updateGrid();
  };

  switchGraphDecoration = function() {
    const colorVar = document.getElementById('color').value;

    if (colorVar === 'None') {
      grid.classList.add('noBorder');
    } else {
      grid.classList.remove('noBorder');
    }

    graphs.color.update(colorVar);

    updateGrid();
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

  updateElementById('crit1', generateSelect(vars, 'depth'));
  updateElementById('crit2', generateSelect(vars, 'star_nodes'));
  updateElementById('color', generateSelect([...vars, 'None'], 'None'));

  reorderGrid();
  changeImageSize(150);
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

      if (typeof(this.color) !== 'undefined') {
        this.addColor(this.color.value);
      }
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

    graphsArr.forEach(function(graph) {
      elements.appendChild(graph.cloneNode(true));
    });

    return Array.prototype.slice.call(elements.children);
  };
  this.addColor = (crit) => {
    if (crit == 'None') { return }

    if (this.mode.value === 'list') {
      this.graphsArr = colorGraphs(this.graphsArr, crit, this.vars[crit]);
    } else {
      this.arrangeAsTable();
    }
  };
  this.changeSize = (value) => {
    this.graphsArr.forEach(function(tree) {
      tree.style.width = value + 'px';
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

      if (this.color.value !== 'None') {
        trees = colorGraphs(trees, this.color.value, this.vars[this.color.value]);
      }

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
  this.color = new Control('None', this.addColor);
  this.mode = new Control('list', this.changeMode);
  this.imgSize = new Control(150, this.changeSize);
}

colorGraphs = (graphsArr, crit, values) => {
  var critValues = values.sort(sortNumbers),
      step = 0.9/critValues.length,
      seq = range(0.1, 1, step),
      colorArr = {},
      colors = interpolateColors('rgb(244, 161, 66)', 'rgb(189, 22, 226)', critValues.length);

  critValues.forEach((key, i) => colorArr[key] = colors[i]);

  var lastValue = null;
  graphsArr.forEach(function(tree) {
    color = colorArr[tree.dataset[crit]];
    tree.style['border-bottom'] = '2px solid rgba(' + color.join(', ') + ')';

    if (tree.dataset[crit] != lastValue) {
      tree.dataset.label = tree.dataset[crit];
      tree.classList.add('label');
      lastValue = tree.dataset[crit];
    } else {
      tree.classList.remove('label');
    }
  });

  return graphsArr;
};

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

displayToolTip = function(element) {
  var text = '',
      tooltip = document.getElementById('tooltip'),
      elements = document.createDocumentFragment();

  Object.keys(element.dataset).forEach((key) => {
    var li = document.createElement('li');

    li.innerHTML = key + ': ' + element.dataset[key];
    elements.appendChild(li);
  });

  var ul = document.createElement('ul');
  ul.appendChild(elements);

  tooltip.innerHTML = null
  tooltip.appendChild(ul);
  tooltip.classList.remove('hidden');
};

hideToolTip = function() {
  var tooltip = document.getElementById('tooltip');
  tooltip.classList.add('hidden');
};

interpolateColor = function(color1, color2, factor) {
    if (arguments.length < 3) { 
        factor = 0.5; 
    }
    var result = color1.slice();
    for (var i = 0; i < 3; i++) {
        result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
    }
    return result;
};

interpolateColors = function (color1, color2, steps) {
    var stepFactor = 1 / (steps - 1),
        interpolatedColorArray = [];

    color1 = color1.match(/\d+/g).map(Number);
    color2 = color2.match(/\d+/g).map(Number);

    for(var i = 0; i < steps; i++) {
        interpolatedColorArray.push(interpolateColor(color1, color2, stepFactor * i));
    }

    return interpolatedColorArray;
};
