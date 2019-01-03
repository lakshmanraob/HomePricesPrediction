Twitter configuration can be done, by replacing the consumer_key, consumer_secret, access_token, access_token_secret in settings.json file
1. The filter text is available inside the code
2. The script by default fetch tweets for 1 minute from the launch time, can be configurable for the specific time as well
3. Once the tweets are fetched it will get create the data frame
4. The analysis will be done on the data frame
    1. Clean the tweets for further processing
        1. Stopwords
        2. Excluding the html and ‘RT’
        3. Analyze the sentiment for the tweet as well
        4. Create the Word Cloud for the tweets
        5. Give the analysis for the captured tweets