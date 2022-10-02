import csv
import sys

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
    # directory = "small"
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

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    """
        BFS algorithm
        take current ID, list neighboring movies. For every movie, list every star. If they are not in visited, add them to the q.
        Run BFS on the first star in the q. If the star is the target, return the route. If not, add the star to visited and run BFS on the next star in the q.
    """
    #Recursive Attempt - times out on Large
    # visited = []    
    # def bfs(route, q):
    #     if not q:
    #         return None
    #     mId, curId = q.pop(0)
    #     if curId == target:
    #         route.append((mId, curId))
    #         return route
    #     visited.append(curId)
    #     for n in neighbors_for_person(curId):
    #         if n[1] not in visited and n not in q:
    #             q.append(n)
    #     if curId != source: route.append((mId, curId))
    #     return bfs(route, q)
    # print(people[source]["movies"])
    # initMov = list(people[source]["movies"])[0]
    # return bfs([], [(initMov, source)])
    
    #Iterative Attempt
    
    start = Node(source, None, None)
    qf = QueueFrontier()
    qf.add(start)
    visited = set()
    
    #BFS algorithm - use the Node since it can save the route taken
    while True:
        if qf.empty():
            return None
        node = qf.remove()
        visited.add(node.state)
        for n in neighbors_for_person(node.state):
            #Checks to see if the neighbor is not already in the queue or already visited
            if not qf.contains_state(n[1]) and not n[1] in visited:
                curNode = Node(n[1], node, n[0])
                if curNode.state == target:
                    route = []
                    while curNode.parent is not None:
                        route.append((curNode.action, curNode.state))
                        curNode = curNode.parent
                    route.reverse()
                    return route
                qf.add(curNode)
        

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
