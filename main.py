# MOVIE SUGGESTION SYSTEM

from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import requests

print("WELCOME TO PYBOXD!")
print("Data used for predictions: overview, genre, and director of the movie.")
print("Prediction: Movies that you are curious about categorised as Like/Probably Like/Probably Dislike/Dislike")
print("Also Predicts top 20 rated movies on the entire database that you will enjoy")
print("Please be careful to input a movie title as it is! Happy Testing and Happy Watching! - Dania :)")
print()

# APIKey I got by making a developer account at The Movie Database.
APIKey = "34468f2d581c51dd77100d646c457fab"

# Overview, Genre IDs, and Director Name for each movie stored here for training the machine
training_texts = []

# Overview, Genre IDs, and Director Name for each movie the user is curious about stored here for machine to make a decision
tobetested_texts = []

# Titles of the top rated 20 movies on The Movie Database
mostpopular_titles = []

# Overview, Genre IDs, and Director Name for the top 20 rated movies stored here for machine to make a decision
mostpopular_texts = []

# INPUT 

'''
# The following lines are for taking input for the user and populating the arrays initialized above. 
i = int(input("How many movies that you like are you entering?"))

for x in range(i):
  movieName = input("Enter the name of a movie you like: ")
  positive_titles.append(movieName)

print()

i = int(input("How many movies that you dislike are you entering? "))

for x in range(i):
  movieName = input("Enter the name of a movie you didn't like: ")
  negative_titles.append(movieName)

print()

i = int(input("How many movies that you're curious about are you entering?"))

for x in range(i):
  movieName = input("Enter the name of a movie you're curious about: ")
  tobetested.append(movieName)
  
'''

# Testing Set Values
negative_titles = ["Avatar", "1917", "Joker", "Inception", "Interstellar", "The Platform", "Titanic", "The Wolf of Wall Street"]

positive_titles = ["Toy Story", "Big Hero 6", "Trolls World Tour", "Jumanji: The Next Level", "Tangled", "Despicable Me 2", "Finding Nemo", "Garfield", "Toy Story 2"]

tobetested = ["Aladdin", "Frozen", "Coco", "Mad Max: Fury Road", "Pets 2", "Incredibles 2", "Scream", "Zootopia", "Inside Out", "Top Gun: Maverick", "Trolls", "Shrek"]

# ALGORITHM
# Goes through the movies that the user likes and pulls the above mentioned parameters from The Movie Database to store in training_texts[]
for x in range(len(positive_titles)):
  directors = []
  movieName = positive_titles[x]
  httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
  response = requests.get(httpRequest)
  data = response.json()
  training_texts.append(data["results"][0]["overview"])
  training_texts.append(str(data["results"][0]["genre_ids"]))

  movie_id = data["results"][0]["id"]
  httpRequest2 = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + APIKey + "&append_to_response=credits"
  response = requests.get(httpRequest2)
  data = response.json()
  hello = data["credits"]
  hello1 = hello["crew"]
  for x in hello1:
    if x["job"] == "Director":
        directors.append(x["name"])
  training_texts.append(str(directors))

# Goes through the movies that the user dislikes and pulls the above mentioned parameters from The Movie Database to store in training_texts[]
for x in range(len(negative_titles)):
  directors = []
  movieName = negative_titles[x]
  httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
  response = requests.get(httpRequest)
  data = response.json()
  training_texts.append(data["results"][0]["overview"])
  training_texts.append(str(data["results"][0]["genre_ids"]))

  movie_id = data["results"][0]["id"]
  httpRequest2 = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + APIKey + "&append_to_response=credits"
  response = requests.get(httpRequest2)
  data = response.json()
  hello = data["credits"]
  hello1 = hello["crew"]
  for x in hello1:
    if x["job"] == "Director":
        directors.append(x["name"])
  training_texts.append(str(directors))

# Goes through the movies that the user is curious about and pulls the above mentioned parameters from The Movie Database to store in tobetested_texts[]
for x in range(len(tobetested)):
  directors = []
  movieName = tobetested[x]
  httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
  response = requests.get(httpRequest)
  data = response.json()
  tobetested_texts.append(data["results"][0]["overview"])
  tobetested_texts.append(str(data["results"][0]["genre_ids"]))

  movie_id = data["results"][0]["id"]
  httpRequest2 = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + APIKey + "&append_to_response=credits"
  response = requests.get(httpRequest2)
  data = response.json()
  hello = data["credits"]
  hello1 = hello["crew"]
  for x in hello1:
    if x["job"] == "Director":
        directors.append(x["name"])
  tobetested_texts.append(str(directors))

# Pulls the parameters for the current 20 top rated movies and puts them in mostpopular_texts[]
directors = []
httpRequest = "https://api.themoviedb.org/3/movie/top_rated?api_key=e20e035943ec00333eb2a1d09ea93a5c&language=en-US&page=1"
response = requests.get(httpRequest)
data = response.json()
bye = data["results"]
for x in bye:
  if x["overview"] != "" or x["genre_ids"] != "":
    mostpopular_titles.append(x["title"])
    mostpopular_texts.append(x["overview"])
    mostpopular_texts.append(str(x["genre_ids"]))
    movie_id = x["id"]
    httpRequest2 = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + APIKey + "&append_to_response=credits"
    response = requests.get(httpRequest2)
    data = response.json()
    hello = data["credits"]
    hello1 = hello["crew"]
    for x in hello1:
      if x["job"] == "Director":
        directors.append(x["name"])
    mostpopular_texts.append(str(directors))

# Prepare an equivalent set of labels, to tell the machine that the first texts that came from the users likes are positive and the rest are negative
# When I feed these into the classifier, it will use indices to match up
training_labels = ["good"] * (3*len(positive_titles)) + ["bad"] * (3*len(negative_titles))

#The vectorizer is set up here : the first main component of machine learning
vectorizer = CountVectorizer(stop_words='english')

# Here I feed the data we have into the vectorizer so it can keep a Consistent Mapping
vectorizer.fit(training_texts)

# Here I transform all of the training texts into vector form
# Basically makes it a list of numbers because code makes decisions quantitatively
training_vectors = vectorizer.transform(training_texts)

# Convert the texts we are going to test and classify as good and bad into vector form
test_texts = tobetested_texts
test_populartexts = mostpopular_texts
testing_vectors = vectorizer.transform(test_texts)
testing_vectors_popular = vectorizer.transform(test_populartexts)

# This is where the real machine learning happens as the code "connects the dots"
# Between the training data and what is considered good and bad using the labels.
classifier = tree.DecisionTreeClassifier()
classifier.fit(training_vectors, training_labels)

# Uses the connections the code made in previous steps
# To test each of the parameters of each movie the user wants to test and returns if the user will like it or not
likeDict = {
  "like" : "",
  "will probably like" : "",
  "will probably dislike" : "",
  "dislike" : ""
}

print("Recommendations based on movies inputted:")
print()
for i, movie in enumerate(tobetested):
  listFormat = [tobetested_texts[i*3], tobetested_texts[i*3+1], tobetested_texts[i*3+2]]
  vectorFormat = vectorizer.transform(listFormat)
  result = classifier.predict(vectorFormat)
  if result[0] == 'good' and result [1] == 'good' and result[2] == 'good':
    likeDict['like'] += (movie + ", ")
  elif result[0] == 'bad' and result [1] == 'bad' and result[2] == 'bad':
    likeDict['dislike'] += (movie + ", ")
  elif result[0] == 'good' and result [1] == 'good' and result[2] == 'bad':
    likeDict['will probably like'] += (movie + ", ")
  elif result[0] == 'bad' and result [1] == 'good' and result[2] == 'good':
    likeDict['will probably like'] += (movie + ", ")
  elif result[0] == 'good' and result [1] == 'bad' and result[2] == 'good':
    likeDict['will probably like'] += (movie + ", ")
  else:
    likeDict['will probably dislike'] += (movie + ", ")

for x in likeDict:
  if likeDict[x] != "":
    print("You", x, likeDict[x][0:-2])
    print()
print()
print()

# Uses the connections the code made in previous steps to test each of the parameters of each movies in the top 20 rated list
# Returns if the user will like/not like/probabaly like/probabaly not like based on the results
likeDict = {
  "like" : "",
  "will probably like" : "",
  "will probably dislike" : "",
  "dislike" : ""
}

print("Based on likes and dislikes, top 20 top rated movies in the entire movie database:")
print()
for i, movie in enumerate(mostpopular_titles):
  listFormat = [mostpopular_texts[i*3], mostpopular_texts[i*3+1], mostpopular_texts[i*3+2]]
  vectorFormat = vectorizer.transform(listFormat)
  result = classifier.predict(vectorFormat)
  if result[0] == 'good' and result [1] == 'good' and result[2] == 'good':
    likeDict['like'] += (movie + ", ")
  elif result[0] == 'bad' and result [1] == 'bad' and result[2] == 'bad':
    likeDict['dislike'] += (movie + ", ")
  elif result[0] == 'good' and result [1] == 'good' and result[2] == 'bad':
    likeDict['will probably like'] += (movie + ", ")
  elif result[0] == 'bad' and result [1] == 'good' and result[2] == 'good':
    likeDict['will probably like'] += (movie + ", ")
  elif result[0] == 'good' and result [1] == 'bad' and result[2] == 'good':
    likeDict['will probably like'] += (movie + ", ")
  else:
    likeDict['will probably dislike'] += (movie + ", ")

for x in likeDict:
  if likeDict[x] != "":
    print("You", x, likeDict[x][0:-2])
    print()

# Looking at how the code makes its decisions visually is a lot easier so I export the model to the db.dot file
# Upon copying all the data in db.dot and pasting it in the textbox on http://www.webgraphviz.com/
# You can see what the decision making process looks like.
tree.export_graphviz(
    classifier,
    out_file = 'db.dot',
    feature_names = vectorizer.get_feature_names_out(),
    class_names = ["bad","good"]
)
