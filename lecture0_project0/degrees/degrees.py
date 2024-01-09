import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    stack_frontier = StackFrontier()
    queue_frontier = QueueFrontier()
    
        # Start the timer for StackFrontier
    start_time_stack = time.time()
    # Perform the search operation with StackFrontier
    stack_path = shortest_path(source, target, stack_frontier)
    # Stop the timer and calculate the elapsed time
    elapsed_time_stack = time.time() - start_time_stack

    # Start the timer for QueueFrontier
    start_time_queue = time.time()
    # Perform the search operation with QueueFrontier
    queue_path = shortest_path(source, target, queue_frontier)
    # Stop the timer and calculate the elapsed time
    elapsed_time_queue = time.time() - start_time_queue

    # Calculate the time difference
    time_difference = abs(elapsed_time_stack - elapsed_time_queue)
    print("Stack time is:", elapsed_time_stack, "with", len(stack_path), "degrees of separation.")
    print("Queue time is:", elapsed_time_queue, "with", len(queue_path), "degrees of separation.")
    print("Time difference is:", time_difference, "seconds.")
    
    # Choose the approach with the least degrees of separation
    if len(stack_path) < len(queue_path):
        chosen_path = stack_path
        print("Chosen method: StackFrontier")
    else:
        chosen_path = queue_path
        print("Chosen method: QueueFrontier")

    # Print the degrees of separation
    degrees = len(chosen_path)
    print(f"{degrees} degrees of separation.")
    chosen_path = [(None, source)] + chosen_path
    for i in range(degrees):
        person1 = people[chosen_path[i][1]]["name"]
        person2 = people[chosen_path[i + 1][1]]["name"]
        movie = movies[chosen_path[i + 1][0]]["title"]
        print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target, frontier):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Keep track of number of states explored
    num_explored = 0
    
    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    frontier.add(start)
    
    # Initialize an empty explored set
    explored = set()
    
    # Keep looping until solution found
    while True:
        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")
        
        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1
        
        # Mark node as explored
        explored.add(node.state)
        
        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)
                
                # If node is the goal, then we have a solution
                if child.state == target:
                    movies = []
                    people = []
                    solution = []
                    path = []
                    while child.parent is not None:
                        movies.append(child.action)
                        people.append(child.state)
                        child = child.parent # move to the next node
                    movies.reverse()
                    people.reverse()
                    x = zip(movies, people)
                    for movie, person in x:
                        solution.append((movie, person))     
                    return solution


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
