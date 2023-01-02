# Name: Jawaad Ahmar
# Student#: 251237757
# UWO email: jahmar@uwo.ca



# this program inputs a file containing keywords and a file containing tweets
# sentiment_analysis.py computes the happiness scores of each region
# sentiment_analysis.py returns a list of tuples containg the average happiness scores, number of keyword tweets, and total tweets for each region
# main.py prompts the user for input until a valid file name is entered or the number 0
# main.py then formats the output and prints it out



# import compute_tweets function from sentiment_analysis
from sentiment_analysis import compute_tweets



# set terminate bool equal to False
terminate = False

# while loop loops until the user enters a valid input or if user enters 0
while terminate == False:

    # input tweets file
    inFile_tweets = input("Enter the name of the file containing the tweets: ")
    if inFile_tweets == "0":
        print("Thanks.")
        terminate = True
    else:

        # input keywords file
        inFile_keywords = input("Enter the name of the file containing the keywords: ")
        if inFile_keywords == "0":
            print("Thanks.")
            terminate = True
        else:

            # try catch loop loops until user enters a existent files
            try:

                # open files and assign to variables
                fileName_tweets = open(inFile_tweets, "r", encoding="utf-8")
                fileName_keywords = open(inFile_keywords,"r", encoding="utf-8")

                # assign compute_tweets function to variable
                output = compute_tweets(fileName_tweets, fileName_keywords)

                # format output
                print("| Eastern |")
                print("Average:", output[0][0], " Keyword Tweets:", output[0][1], " Total Tweets:", output[0][2],"\n")
                print("| Central |")
                print("Average:", output[1][0], " Keyword Tweets:", output[1][1], " Total Tweets:", output[1][2],"\n")
                print("| Mountain |")
                print("Average:", output[2][0], " Keyword Tweets:", output[2][1], " Total Tweets:", output[2][2],"\n")
                print("| Pacific |")
                print("Average:", output[3][0], " Keyword Tweets:", output[3][1], " Total Tweets:", output[3][2],"\n")
                terminate = True

            # exception file not found error if user enters a file that does not exist
            except FileNotFoundError:
                print("Non-existent file(s).")
                print("Try again.")
                terminate = False