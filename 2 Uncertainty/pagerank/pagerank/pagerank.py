import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probs = {}
    if len(corpus[page]) == 0:
        for k in corpus.keys():
            probs[k] = 1/len(corpus.keys())
        return probs
    for k in corpus.keys():
        probs[k] = (1-damping_factor)/len(corpus.keys())
    links = corpus[page]
    for l in links:
        probs[l] += damping_factor/len(links)
    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    
    #first sample
    for k in corpus.keys():
        ranks[k] = 0
    
    trans = transition_model(corpus, random.choice(list(ranks.keys())), damping_factor)
    curPage = choose_page(trans)
    ranks[curPage] += 1
    while n-1 >0:
        trans = transition_model(corpus, curPage, damping_factor)
        curPage = choose_page(trans)
        ranks[curPage] += 1
        n-=1
    sumAll = sum(ranks.values())
    for k in ranks.keys():
        ranks[k] /= sumAll
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print(corpus)
    N = len(corpus)
    ranks = {}
    for k in corpus.keys():
        ranks[k] = 1/N
    maxDiff = 1
    while maxDiff > 0.001:
        diffs = []
        for k in corpus:
            prev = ranks[k]
            new = (1-damping_factor)/N
            sums = 0
            for p in corpus:
                if k in corpus[p]:
                    sums += ranks[p]/len(corpus[p])
            new += damping_factor*sums
            diffs.append(abs(prev-ranks[k]))
            ranks[k] = new
        maxDiff = max(diffs)
            
    return ranks
def choose_page(trans):
    return random.choices(list(trans.keys()), weights=trans.values(), k=1)[0]

if __name__ == "__main__":
    main()
