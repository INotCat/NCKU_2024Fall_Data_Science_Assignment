# list of dictionary data structure to store the data reading from csv file into the program
data = []
try:
    with open('IMDB-Movie-Data.csv', 'r') as file:
        headers = file.readline().strip().split(',')
        #print(headers)
        for line in file:
            values = line.strip().split(',')
            values = [value if value != '' else '-1' for value in values]
            row_dict = dict(zip(headers, values))
            data.append(row_dict)           
except FileNotFoundError:
    print('File not found. Please check the file path.')
except Exception as e:
    print(f'An error occurred: {e}')

data_size = len(data)   


# First: I find the top3 value first, 
# Second: And then iterate again if any movie match the chosen rating value, append 
# the corresponding movie name to be the answer
def find_top3_rating_movies() -> list:
    top3_value = [-10,-10,-10]
    for i in range(0,data_size):
        if data[i]['Year'] == '2016':
            value = float(data[i]['Rating'])
            if value > top3_value[0]:
                top3_value[2] = top3_value[1]
                top3_value[1] = top3_value[0]
                top3_value[0] = value
            elif value > top3_value[1] and value != top3_value[0]:
                top3_value[2] = top3_value[1]
                top3_value[1] = value
            elif value > top3_value[2] and value != top3_value[1] and top3_value[0]:
                top3_value[2] = value
    
    T0 = []
    T1 = []
    T2 = []
    for i in range(0,data_size):
        if data[i]['Year'] == '2016':
            if float(data[i]['Rating']) == top3_value[0]: 
                T0.append(data[i]['Title'],)    
            elif float(data[i]['Rating']) == top3_value[1]:  
                T1.append(data[i]['Title']) 
            elif float(data[i]['Rating']) == top3_value[2]: 
                T2.append(data[i]['Title'])   

    return T0,T1,T2


# First: I store actor, the number of movie he/she featured, and the total revenue
# Second: And then I dynamically replacing the top1 average revenue and updating the top1 actor simultaneously
# my average revenue = total money of the movie the actor featured / the number of the movie
##(I did not count in the movie whose revenue is not recorded in the csv data)
def find_top1_avgRevenue_actor() -> list:
    actor_to_avgRevenue_dict = {} #{'Name':[movie_count,revenu]}

    for i in range(0,data_size):     
        actors = [actor.strip() for actor in data[i]['Actors'].split('|')]
        
        revenue = float(data[i]['Revenue (Millions)'])
        
        if revenue == -1.0:
            continue
        
        for actor in actors:
            if actor not in actor_to_avgRevenue_dict:
                actor_to_avgRevenue_dict[actor] = [0,0]
            
            actor_to_avgRevenue_dict[actor][0] += 1 
            actor_to_avgRevenue_dict[actor][1] += revenue
        
    top1_avg_revenue = -1
    top1_actor = []
    for actor, (movie_count, total_revenue) in actor_to_avgRevenue_dict.items():
        if movie_count > 0:
            avg_revenue = total_revenue / movie_count
        else:
            avg_revenue = 0
    
        if avg_revenue > top1_avg_revenue:
            top1_actor = []
            top1_avg_revenue = avg_revenue
            top1_actor.append(actor)
        elif avg_revenue == top1_avg_revenue:
            top1_actor.append(actor)
            
    return top1_actor


# find the total rating of a giving actor/actress and then divided the number of the movie he/she featured
def avg_rating_for_actor(name: str) -> float:
    count = 0
    rating_sum = 0
    for i in range(0,data_size):
        actors = [actor.strip() for actor in data[i]['Actors'].split('|')]
        if name in actors:
            if data[i]['Rating'] == '-1':
                continue
            count += 1
            rating_sum += float(data[i]['Rating'])

    return rating_sum / count if count != 0 else 0


# First: I find handle the data to be {director1:(actor1,actor2,...),director2:(acotr1,actor2,...),...}
# Second: And then iterate this dictionary again to find the top3 director whose length of set are 
# top3 in the dictionary
def find_top3_directors_collborating_with_actors(): 
    director_to_actorNameSet_dic = {}
    for i in range(0, data_size):
        director = data[i]['Director']
        actors = [actor.strip() for actor in data[i]['Actors'].split('|')]

        if director not in director_to_actorNameSet_dic:
            director_to_actorNameSet_dic[director] = set()
        
        director_to_actorNameSet_dic[director].update(actors)

    top3_counts = [-1, -1, -1]
    # Find the top 3 directors based on unique actor counts
    for director, actors_set in director_to_actorNameSet_dic.items():
        count = len(actors_set)
        
        if count > top3_counts[0]:
            top3_counts[2] = top3_counts[1]
            top3_counts[1] = top3_counts[0]
            top3_counts[0] = count

        elif count > top3_counts[1] and count != top3_counts[0]:
            top3_counts[2] = top3_counts[1]
            top3_counts[1] = count

        elif count > top3_counts[2] and count != top3_counts[0] and count != top3_counts[1]:
            top3_counts[2] = count

    T0 = []
    T1 = []
    T2 = []
    for director, actors_set in director_to_actorNameSet_dic.items():
        
        if len(actors_set) == top3_counts[0]:
            T0.append(director)
        elif len(actors_set) == top3_counts[1]:
            T1.append(director)
        elif len(actors_set) == top3_counts[2]:
            T2.append(director)
  
    return T0, T1, T2
   
# First: I find handle the data to be just like what I do above in find_top3_directors_collborating_with_actors()
# Second: And then iterate the dictionary, and find top2 length of the set     
def find_top2_actor_playing_most_genres() -> list:
    actor_to_genres_dic = {}
    
    for i in range(0, data_size):
        actors = [actor.strip() for actor in data[i]['Actors'].split('|')]
        
        for actor in actors:
            if actor not in actor_to_genres_dic:
                actor_to_genres_dic[actor] = set()
            actor_to_genres_dic[actor].update(set(data[i]['Genre'].split('|')))
                 
    T0 = []       
    T1 = []    
    top2_count = [-1,-1]
    for actor, genere in actor_to_genres_dic.items():
        g_size = len(genere)
        if g_size > top2_count[0]:
            top2_count[1] = top2_count[0]
            top2_count[0] = g_size
        elif g_size > top2_count[1] and g_size != top2_count[0]:
            top2_count[1] = g_size

    for actor, genere in actor_to_genres_dic.items():
        g_size = len(genere)
        if g_size == top2_count[0]:
            T0.append(actor)
        elif g_size == top2_count[1]:
            T1.append(actor)

    return T0, T1

# First: I find handle the data to be {actor1:(year1,year2,...),actor2:(year1,year2,...),...)
# Second: sort each set for the actor and count ther max_gap 
# Third: find the max_gap among the actors in the dictionary and ouput the corresponding name
def find_actors_with_largest_max_gap_year() -> list:
    actor_to_movieAndYear = {}
    
    for i in range(0,data_size):
        actors = [actor.strip() for actor in data[i]['Actors'].split('|')]
        clean_actors = [actor.strip() for actor in actors]

        for actor in clean_actors:
            if actor not in actor_to_movieAndYear:
                actor_to_movieAndYear[actor] = set()
            
            actor_to_movieAndYear[actor].update([data[i]['Year']])
    
    T0 = []
    max_gap_year = -1
    
    for actor, years in actor_to_movieAndYear.items():
        sorted_years = sorted(list(years))

        gap = int(sorted_years[-1]) - int(sorted_years[0])
        if gap > max_gap_year:
            max_gap_year = gap
            T0 = []
            T0.append(actor)
        elif gap == max_gap_year:
            T0.append(actor)

    return T0 
    
    

def create_collaborations(namelist: str) -> dict:
    collaborations = {}
    names = [name.strip() for name in namelist.split('|')]

    for name in names:
        if name not in collaborations:
            collaborations[name] = set()
        
        for collaborator in names:
            if collaborator != name:
                collaborations[name].add(collaborator)
                if collaborator not in collaborations:
                    collaborations[collaborator] = set()
                collaborations[collaborator].add(name)  # Ensure bidirectional collaboration
    return collaborations

def combine_two_dict(combined_dict : dict, other: dict) -> dict:

    for key, value in other.items():
        if key not in combined_dict:
            combined_dict[key] = value.copy()
        else:
            ####union return a set or update change the set in place and more efficient said by gpt
            combined_dict[key].update(value)
    return combined_dict

def find_collaborators(all_collab_dic: dict, name: str) -> set:
    
    stack = list(all_collab_dic[name])
    result_set = all_collab_dic[name].copy()
    visited_set = all_collab_dic[name].copy()
    visited_set.add(name)
    
    while stack:
        direct = stack.pop()
        for indirect in all_collab_dic[direct]:
            if indirect not in visited_set:
                result_set.add(indirect)
                visited_set.add(indirect)
                stack.append(indirect)

    return result_set
   
# First: I create many dictionary 'each' acotr has its all direct and indirect collaborators in a set
    #via create_collaborations()
# Second: I combine each dictionary small dict to a large dict {actor1:(collab1,collab2,..),actor2:(collab1,collab2,..)...}
    #via  combine_two_dict()
# Third: using DFS, I use a set to record who has been visited, and a stack is for a waiting list.
    #find the small dictionary according to the list and do update.method(like union operation)
    #via find_collaborators()
def find_actor_collaborate_with_N(name: str) -> set:
    all_collab = {}
    for i in range(0,data_size):
        all_collab = combine_two_dict(all_collab,create_collaborations(data[i]['Actors'])) 
        
    return find_collaborators(all_collab, name)
    
    

# Rank,Title,Genre,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
print('Q1: Top-3 movies with the highest ratings in 2016?')
top3_movies_1, top3_movies_2, top3_movies_3 = find_top3_rating_movies()
print("top1: "+ "".join(top3_movies_1))
print("top2: "+ "".join(top3_movies_2))
print("top3: "+ "".join(top3_movies_3))
print()

print('Q2: The actor generating the highest average revenue?')
top1_avgRevenue_actor = find_top1_avgRevenue_actor()
print("\n".join(top1_avgRevenue_actor))
print()

print('Q3: The average rating of Emma Watson’s movies?') 
print(avg_rating_for_actor('Emma Watson')) 
print()

print('Q4: Top-3 directors who collaborate with the most actors?')
top3_director_1, top3_director_2, top3_director_3 = find_top3_directors_collborating_with_actors()
print("top1:\n" + "\n".join(top3_director_1))
print("top2:\n" + "\n".join(top3_director_2))
print("top3:\n" + "\n".join(top3_director_3))
print()

print('Q5: Top-2 actors playing in the most genres of movies?')
actors_most_genres_1, actors_most_genres_2 = find_top2_actor_playing_most_genres()
actors_most_genres_1 = sorted(actors_most_genres_1)
actors_most_genres_2 = sorted(actors_most_genres_2)
print("top1:\n"+"\n".join(actors_most_genres_1))
print("top2:\n"+"\n".join(actors_most_genres_2))
print() 
 
print('Q6: Top-1 actor whose movies lead to the largest maximum gap of years?')
actors_max_gap = sorted(find_actors_with_largest_max_gap_year())
print(f"There are {len(actors_max_gap)} people:")
print("\n".join(actors_max_gap))
print()

print('Q7: Find all actors who collaborate with Johnny Depp in direct and indirect ways')
collaborate_with_johnny_deep = sorted(find_actor_collaborate_with_N('Johnny Depp'))
print(f"There are {len(collaborate_with_johnny_deep)} people:")
print("\n".join(collaborate_with_johnny_deep))


      