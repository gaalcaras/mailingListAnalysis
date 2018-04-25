import os
from tqdm import tqdm

def gridgraph(ml, thread_ids, title):
    draw_trees(ml, thread_ids)
    body = ''

    for thread in thread_ids:
        body += tree_img(ml.thread(thread))

    make_page('assets/html/{}.html'.format(title), title, body)

def tree_img(thread):
    img = '<a href="http://public-inbox.org/git/{}"'.format(thread.data['thread'])
    img += ' target="_blank"'
    img += ' title="{}"'.format(thread.data['subject'])
    img += '>'
    img += '<img'

    for k, v in thread.data.items():
        img += ' data-{}="{}"'.format(k, v)

    img += ' src="../img/tree/{}.svg"'.format(thread.data['thread'])
    img += ' alt="{}"'.format(thread.data['thread'])
    img += '/></a>'

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
  <title>{}</title>
</head>

<body>
<h1>title</h1>
{}
</body>
</html>
    """.format(title, body)

    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as page:
        page.write(template)
