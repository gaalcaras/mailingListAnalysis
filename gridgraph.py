import os
from tqdm import tqdm

def gridgraph(ml, thread_ids, title):
    draw_trees(ml, thread_ids)
    body = ''

    for thread in thread_ids:
        body += tree_img(ml.thread(thread))

    make_page('assets/html/{}.html'.format(title), title, body)

def tree_img(thread):
    img = '<span class="tree"'
    for k, v in thread.data.items():
        img += ' data-{}="{}"'.format(k, v)

    img += '>\n'

    img += '<a href="http://public-inbox.org/git/{}"'.format(thread.data['thread'])
    img += ' target="_blank"'
    img += ' title="{}"'.format(thread.data['subject'])
    img += '>\n'
    img += '<img'

    img += ' src="../img/tree/{}.svg"'.format(thread.data['thread'])
    img += ' alt="{}"'.format(thread.data['thread'])
    img += '/>\n</a>\n'
    img += '</span>\n'

    return img

def draw_trees(ml, thread_ids):
    """Draw trees for each thread.

    :ml: MailingList object storing the threads
    :thread_ids: list of thread IDs
    """

    for thread in tqdm(thread_ids, desc='Generating tree images'):
        ml.thread(thread).draw_tree(save=True)

def make_page(filepath, title, body):
    """Create HTML page.

    :filepath: target html file
    :title: page title
    :body: content of the page
    """

    template = """<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="../js/gridgraph.js"></script>
  <link rel="stylesheet" type="text/css" href="../css/gridgraph.css"><Paste>
  <title>{}</title>
</head>

<body>
<div id="controls">
<form>
<fieldset>
<p>
<label>Image size</label>
<input type="range" min="100" max="500" step="10" value="300" id="img-size" oninput="changeImageSize(this.value)">
</p>
</fieldset>
</form>
</div>
<div id="grid">
{}
</div>
</body>
</html>
    """.format(title, body)

    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as page:
        page.write(template)
