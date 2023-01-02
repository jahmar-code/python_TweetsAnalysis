
# compute_tweets function inputs tweets file and keywords file and returns a list of tuples based on location
def compute_tweets(fileName_tweets,fileName_keywords):

    # declare lists for each timezone
    eastern_dict = {}
    central_dict = {}
    mountain_dict = {}
    pacific_dict = {}
    none_dict = {}

    # declare lists to create keyword_array
    keywordWORD_list= []
    keywordVALUE_list = []

    # declare lists to create tweet_array
    tweetLOCATION_list = []
    tweetSTRING_list = []



    # for loop iterates through keywords file
    for line_keywords in fileName_keywords:
        keyword = line_keywords.split(",")
        keyword_word = keyword[0]
        keyword_value = keyword[1]
        keyword_value = keyword_value.rstrip("\n")
        keywordWORD_list.append(keyword_word)
        keywordVALUE_list.append(keyword_value)

    # make keyword_array global so it is in the scope of other functions
    global keyword_array

    # create an array including keywords and their values
    keyword_array = zip(keywordWORD_list,keywordVALUE_list)
    keyword_array = [list(x) for x in keyword_array]


    # for loop iterates through tweets file
    for line_tweet in fileName_tweets:
        tweet = line_tweet.split()
        tweet[-1] = str(tweet[-1]).strip(",.?! ")
        tweet_string = tweet[5:]
        tweet_string = " ".join(tweet_string)
        tweet_string = remove_punctuation(tweet_string)
        tweet_string = tweet_string.split()
        tweet_locationLAT = tweet[1]
        tweet_locationLONG = tweet[0]
        tweet_locationLONG = tweet_locationLONG.strip("-[],")
        tweet_locationLAT = tweet_locationLAT.strip("-[],")
        tweet_location = (tweet_locationLONG, tweet_locationLAT)
        tweetLOCATION_list.append(tweet_location)
        tweetSTRING_list.append(tweet_string)

    # create an array including tweets and their locations
    tweet_array = zip(tweetLOCATION_list,tweetSTRING_list)
    tweet_array = [list(x) for x in tweet_array]


    # for loop iterates through array of tweets and appends tweets depending on their locations
    tweet_counter = 1
    for i in tweet_array:
        if float(i[0][0]) >= 24.660845 and float(i[0][0]) <= 49.189787:
            if float(i[0][1]) > 67.444574 and float(i[0][1]) <= 87.518395:
                tweet_key = "tweet#" + str(tweet_counter)
                tweet_counter += 1
                eastern_dict.update(dict({tweet_key: i[1]}))

            elif float(i[0][1]) > 87.518395 and float(i[0][1]) <= 101.998892:
                tweet_key = "tweet#" + str(tweet_counter)
                tweet_counter += 1
                central_dict.update(dict({tweet_key: i[1]}))

            elif float(i[0][1]) > 101.998892 and float(i[0][1]) <= 115.236428:
                tweet_key = "tweet#" + str(tweet_counter)
                tweet_counter += 1
                mountain_dict.update(dict({tweet_key: i[1]}))

            elif float(i[0][1]) > 115.236428 and float(i[0][1]) <= 125.242264:
                tweet_key = "tweet#" + str(tweet_counter)
                tweet_counter += 1
                pacific_dict.update(dict({tweet_key: i[1]}))

            else:
                tweet_key = "tweet#" + str(tweet_counter)
                tweet_counter += 1
                none_dict.update(dict({tweet_key: i[1]}))

        else:
            tweet_key = "tweet#" + str(tweet_counter)
            tweet_counter += 1
            none_dict.update(dict({tweet_key: i[1]}))


    # call sentiment_value function with each region in the parameter and assign each return value to a variable
    eastern_function = sentiment_value(eastern_dict)
    central_function = sentiment_value(central_dict)
    mountain_function = sentiment_value(mountain_dict)
    pacific_function = sentiment_value(pacific_dict)


    # create a list of tuples that will return tuple from each location
    TOTAL_RETURN_LIST = [eastern_function, central_function, mountain_function, pacific_function]


    # return list of tuples
    return TOTAL_RETURN_LIST



# sentiment value function iterates through each location's dictionary, computes, and returns a tuple
def sentiment_value(timezone_dict):

    # declare list and set that will store the values of each location's "sentiment" and number of keyword tweets - respectively
    TIMEZONEsentiment_list = []
    TIMEZONEsentimentTWEETS_list = set()


    # for loop iterates through dictionary and appends keyword tweets to a set
    for key, tweet in timezone_dict.items():
        for word in tweet:
            for keyword in keyword_array:
                if word.lower() == keyword[0]:
                    TIMEZONEsentimentTWEETS_list.add(key)

    # for loop iterates through dictionary and appends happiness scores to a list
    for key, tweet in timezone_dict.items():
        if key in TIMEZONEsentimentTWEETS_list:
            TIMEZONEsentiment_list.append(happiness_score(tweet))

    # convert each happiness score into a float
    TIMEZONEsentiment_list = [float(i) for i in TIMEZONEsentiment_list]

    # calulate the sum of keyword values
    sum_of_integers = sum(TIMEZONEsentiment_list)

    # set average equal to zero so that it is in the scope
    average = 0
    # set conditional so average is not equal to zero to avoid possibly dividing by zero
    if len(TIMEZONEsentimentTWEETS_list) != 0:
        average = sum_of_integers / len(TIMEZONEsentimentTWEETS_list)

    # find length of set containing the keyword tweets
    count_of_keyword_tweets = len(TIMEZONEsentimentTWEETS_list)
    # find length of dictionary containing all tweets
    count_of_tweets = len(timezone_dict)


    # return tuple
    return (average, count_of_keyword_tweets, count_of_tweets)



# remove_punctuation function removes punctuation from words in each tweet
def remove_punctuation(tweet_array):
    punctuation = "`~!@#$%^&*()_-+=[]{}|;:<>,.?/\"\'"
    result = ""
    for char in tweet_array:
        if not char in punctuation:
            result += char
    return result



# happiness_score returns happiness score of each individual tweet
def happiness_score(tweet):
    sentiment_values = []
    counter = 0
    for word in tweet:
        for keyword in keyword_array:
            if word.lower() == keyword[0]:
                sentiment_values.append(keyword[1])
                counter += 1
    sentiment_values = [int(i) for i in sentiment_values]
    sum_of_integers = sum(sentiment_values)
    happiness_score = 0
    if len(sentiment_values) != 0:
        happiness_score = sum_of_integers / counter
    return happiness_score