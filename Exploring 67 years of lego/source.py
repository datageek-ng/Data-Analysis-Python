import pandas as pd
file = open('datasets/git_log_excerpt.csv','r')

read_data = file.read()
print(read_data)

git_log = pd.read_csv( 'datasets/git_log.gz', sep='#', encoding='latin-1', header=None, names=['timestamp', 'author'] )
git_log.head()

# calculating number of commits
number_of_commits =git_log['timestamp'].size

# calculating number of authors
number_of_authors = git_log.dropna(how='any')['author'].unique().size

# printing out the results
print("%s authors committed %s code changes." % (number_of_authors, number_of_commits))

author_commits = git_log.groupby('author').count().sort_values(by='timestamp', ascending=False)
top_10_authors = author_commits.head(10)

# Listing contents of 'top_10_authors'
top_10_authors

# converting the timestamp column
git_log['timestamp'] = pd.to_datetime(git_log['timestamp'], unit='s')
# summarizing the converted timestamp column
git_log.describe()

# determining the first real commit timestamp
first_commit_timestamp = git_log[git_log['author']=='Linus Torvalds'].sort_values(by='timestamp').head(1).reset_index(drop=True).iloc[0,0]
# determining the last sensible commit timestamp
last_commit_timestamp =  pd.to_datetime('today')

# filtering out wrong timestamps
corrected_log = git_log[(git_log['timestamp'] >= first_commit_timestamp) & (git_log['timestamp'] <= last_commit_timestamp)]
# summarizing the corrected timestamp column

corrected_log['timestamp'].describe()


# Counting the no. commits per year
commits_per_year = corrected_log.groupby(
    pd.Grouper(
        key='timestamp',
        freq='AS'
        )
    ).count()

# Listing the first rows

commits_per_year.head()


# Setting up plotting in Jupyter notebooks
%matplotlib inline

# plot the data
commits_per_year.plot(kind='line', legend=False, title='commits per year' )


# calculating or setting the year with the most commits to Linux
year_with_most_commits = 2015
