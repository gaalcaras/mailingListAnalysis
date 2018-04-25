import os
from tqdm import tqdm

def gridgraph(threads, filepath):
    """Generate HTML grid page.

    :threads: dataframe with threads data
    :filepath: path of output HTML file
    """

    # Load HTML template
    with open('assets/html/gridgraph.html', 'r') as temp:
        template = temp.read()

    # Make grid
    grid = ''
    for thread in threads.to_dict(orient='records'):
        grid += span_tree(thread)

    template = template.format(grid=grid)

    # Write to file
    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as page:
        page.write(template)

def span_tree(thread):
    """Generate tree span for grid list.

    :thread: dict of thread data
    """
    # Generate span attributes
    span_att = ''
    for key, value in thread.items():
        span_att += ' data-{}="{}"'.format(key, value)

    thread['span_att'] = span_att

    # Load template
    with open('assets/html/span.html', 'r') as temp:
        span = temp.read()

    span = span.format(**thread)

    return span

def draw_trees(mailing_list, thread_ids):
    """Draw trees for each thread.

    :mailing_list: MailingList object storing the threads
    :thread_ids: list of thread IDs
    """

    for thread in tqdm(thread_ids, desc='Generating tree images'):
        mailing_list.thread(thread).draw_tree(save=True)
