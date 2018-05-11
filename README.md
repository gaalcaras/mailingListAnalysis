# mailingListAnalysis

Various tools to analyze mailing list data, developed during my PhD.

![Visualisation of 60 email threads](assets/img/gridgraph.png)

## Installation

First clone the repo and `cd` into it:

```bash
git clone git@github.com:gaalcaras/mailingListAnalysis.git
cd mailingListAnalysis
```

Install required libraries that are listed in `requirements.txt`. For instance,
using [`pip`](https://pypi.python.org/pypi/pip):

```bash
pip install -r requirements.txt
```

## Directory structure

At the root of the repo, you'll find the modules that you can load in your
scripts to perform your data analysis process, such as `mailinglist.py`.

The subdirectories contain:

+ **assets**: useful non python resources
  + **img**: images of graphs, trees and so on
+ **data**: datasets
+ **output**: directory to save outputs from scripts (mainly html pages and images)
+ **scripts**: scripts to perform data analysis
+ **test**: unit tests to help and maintain the code

## Usage example

You can either run the existing scripts in `scripts` to reproduce some of my results, or you can write your own script using the python modules at the root of the repo.

### Running existing scripts

You can run any of the scripts in `scripts` with `python -m` from **the root of the repo**.

For instance, to run `scripts/03_pca_threads_2017.py`:

```bash
python -m scripts.03_pca_threads_2017
```

### Making your own script

You can use any of the modules in the root directory to write your own script.

```python
from mailinglist import MailingList

# Load the mailing list data (Git mailing list from May 19 2017 to May 25 2017)
git_may_2017 = MailingList('data/test_sample1.csv')

# See the emails data frame
print(git_may_2017.emails)

# Build threads by following replies
git_may_2017.make_threads()

# Process each thread and print the threads data frame
git_may_2017.process_threads()
print(git_may_2017.threads)

# Select a thread and draw its tree
# Pro tip: don't forget to run '%pylab' if you're in the jupyter console
git_may_2017.thread('20170520214233.7183-1-avarab@gmail.com').draw_tree()

# Open the thread in your browser
git_may_2017.thread('20170520214233.7183-1-avarab@gmail.com').open()
```

## Data

### Format

For now, mailingListAnalysis only supports csv files. Relevant columns include:

| Column name | Variable                                                           |
| ----        | ----                                                               |
| date        | Email timestamp                                                    |
| from_email  | Sender's email address                                             |
| msg_id      | Email's [`<Message-ID>`](https://en.wikipedia.org/wiki/Message-ID) |
| in_reply_to | `<Message-ID>` of the message the current email replies to         |

### Included datasets

All included datasets come from the [Git mailing list](https://public-inbox.org/git/). You can find included datasets in the `./data` directory:

| File | Dataset description |
| ---- | ---- |
| `test_thread1.csv` | Small 4 email [thread](https://public-inbox.org/git/20170523195132.s57ikef4romy3n3r@sigill.intra.peff.net) |
| `test_thread2.csv` | Bigger 15 email [thread](https://public-inbox.org/git/tnxy899zzu7.fsf@arm.com/) |
| `test_sample1.csv` | 321 emails (41 threads in total) from 2017-05-19 to 2017-05-25 |
| `threads2017.csv` | All ~2500 threads from the year 2017 |

## Testing

Install and run [`pytest`](https://docs.pytest.org/en/latest/) at the root of
the directory.

If you want to only commit code that passes tests, you should install the git
pre-commit hook by running:

```bash
ln -s ../../test/pre_commit.sh .git/hooks/pre-commit
```
