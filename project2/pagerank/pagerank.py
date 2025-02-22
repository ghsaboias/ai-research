import os
import random
import re
import sys
import copy

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
    probabilities = {}
    
    for page in corpus:
        probabilities[page] = 1 - damping_factor / len(corpus)
        
    for link in corpus[page]:
        probabilities[link] += damping_factor / len(corpus[page])
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    percentages = {}
    
    for page in corpus:
        percentages[page] = 0
    
    # Choose a random page to start
    for i in range(n):
        if i == 0:
            page = random.choice(list(corpus.keys()))
        percentages[page] += 1
        # Get the next sample
        next_sample = transition_model(corpus, page, damping_factor)
         
        # Use the probabilities to choose the next page
        values = list(next_sample.values())
        page = random.choices(list(next_sample.keys()), weights=values)[0]
        
    for i in percentages:
        percentages[i] /= n
        
    return percentages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilities = {page: 1 / len(corpus) for page in corpus}
    
    while True:
        probabilities_copy = copy.deepcopy(probabilities)
        for page in corpus:
            rank = (1 - damping_factor) / len(corpus)
            for linking_page in corpus:
                if page in corpus[linking_page]:
                    rank += damping_factor * probabilities[linking_page] / len(corpus[linking_page])
            probabilities_copy[page] = rank
        
        # Check for convergence
        if all(abs(probabilities_copy[page] - probabilities[page]) < 0.001 for page in corpus):
            break
        probabilities = probabilities_copy

    return probabilities

 
if __name__ == "__main__":
    main()
