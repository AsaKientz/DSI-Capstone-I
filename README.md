# Personality Typists

---
## Myers-Briggs Overview
The Myers-Briggs Type Indicator (MBTI) is a personality assessment tool that describes human behavior as a function of different preferences around the use of perception and judgement.  
The Indicator is a 4-letter type, with each letter representing a preference in one of 4 dichotomies:
- **World Facing:** - Introversion (I) or Extraversion (E)
- **Information Gathering:** - Intuition (N) or Sensing (S)
- **Decision Making:** Thinking (T) or Feeling (F)
- **Structure:** - Judging (J) or Perceiving (P)

Each of the resultant 16 personality types tends to exhibit a set of preferences that is characteristic of that type.

Link for more information about [Myers-Briggs](https://www.myersbriggs.org/my-mbti-personality-type/mbti-basics/home.htm?bhcp=1).

---
## Data Source Description
I used a [Kaggle dataset](https://www.kaggle.com/datasnaek/mbti-type/data#) of discussion forum posts at an MBTI-centered site. It contains posts from over 8000 users. Two columns are present - the self-reported MBTI type of a user (one user per row) and a set of 50 posts for that user, listed as a single string, separated by a triple pipe ‘|||’.

![alt text](/images/df_raw_head.png)

Above: First 20 rows of the raw data.

Below: Partial view of one user's 50-post concatenated test string.

![alt text](/images/df_raw_posts3.png)

I was interested to understand how aspects of personality could be detected from posting activity, and what trends within posts may exist that align with the reported personality types.

---
## Which Personalities Talk About Personalities?
What kind of MBTI Type tends to be attracted to a discussion forum on MBTI types?  
Perhaps understandably, the user base is heavily dominated by Intovert (I) and Intuition (N) types, with the top 4 being 
both (I) and (N) types.  The set of 4 INxx types made up 66% of the user base.

![alt text](/images/post_count_by_type_ei.png)

One theory for the heavy skew in INxx participation could be that these types tend to explore information and patterns deeply, so a site where they can discuss their thoughts and understand personality differences would be very attractive.

Though it seems clear the user frequency distribution is not uniform, a Chi-squared test can confirm this.  With a Null Hypothesis that each of the 16 user types would be uniformly represented in user counts, the Chi-squared p-value of 0.0 allows the Null Hypothesis to be formally rejected.

![alt text](/images/posts_by_user_chi-squared.png)

To explore more why INxx types may be drawn to a site discussing personality types, see [here](https://personalityjunkie.com/infj-infp-intj-intp-modern-life/).

---
## Distrubtion of Post Length by Type
Below are data showing the distribution by each type of the length of posts (in characters).  These data were not normalized by Type frequency, so display the expected difference in count.  Y-axis is in log10 due to order of mangitude differences (driven by user frequency).

Two features stand out with these distributions:
- There is a spike in count when post length is in the 190-200 character range, at the upper tail end of the distribution.  (Note: there is no indication on the source website of a max length for a post.  ENTJs have posts ~ 250 characters)
- The other maxima point exists in the ~50 character range for each type.

![alt text](/images/post_length_hist_by_type.png)


---
## SKLearn - Term Frequency and Inverse Document Frequency (tf-idf)
For a set of documents in a corpus, the tf-idf process finds words in a given document that are less frequent across the other documents (idf) but that are also relatively common in that document (tf).  The product of these two metrics produces a tf-idf score.

### Data Prep and Cleaning
The 8675 rows of data required pre-processing.  For each user, all 50 posts were concatenated into one string.  Specifically, the posts needed to be:
- split into a string of words (remove the '|||')
- grouped by each of the 16 user types and merged into a single string with others of that type

This created 16 documents; one for each MBTI Type.

### **CountVectorizer and TFidfTransformer**
  SKLearn has a "TfidfVecorizer" module that allows computation of tf-idf scores in a single pass.  I chose to use the more split approach - CountVectorizer and TfidfTransformer.  This allowed me to view the top 'n' tf-idf words and their scores across each type and become familiar with both the tool and the validity of the data.
  
  Here are idf values from early in the process:

![alt text](/images/mbti-idf-values.png)

  **Stopwords** - SKLearn stopwords removed ~318 high frequency words from CountVectorizer results.  Many words were still common across most/all types and that didn't pass the "Are you distinct and informative?" test.
  An additional 80+ words were added to a custom stoplist to eliminate non-distinvtive words (e.g., 'type', 'people', 'like', etc.)
  
  Another option is to set the "min_df" option to 2 (eliminates words with tf = 1 in one doc) -> reduced corpus from ~145k words to ~50k words.

  Here are ESTJ tf-idf scores before the custom stopword list was implemented - the top 5 words here appeared in the top 10 of most other documents.
  
![alt text](/images/tf-idf_ESTJ_default_stopwords.png)
 

### **Word Clouds**
  Using tf-idf scoring for top 200 words in each word cloud, I made a string of words to enable creating a word cloud.  This string was generated by multiplying each word's tf-idf score by 1000, rounding to nearest integer, and adding that word this many times to a string with spacing.

  **Note:** It's important to set 'Collocations = False' in the word cloud or duplicate word pairs will appear int he graphic due to repeated proximity and the algorithms calculation of a relationship (e.g. "type type")

**Unsuprisingly, each Type's most common word is their Type.  Note the differences in vocabulary for the ESFJ "Provider" and the INTP "Architect".**

![alt text](/images/word_cloud_ESFJ.png)

![alt text](/images/word_cloud_INTP.png)

**View your type here!**

[ISTJ](/images/word_cloud_ISTJ.png)   [ISFJ](/images/word_cloud_ISFJ.png)   [INFJ](/images/word_cloud_INFJ.png)   [INTJ](/images/word_cloud_INTJ.png)

[ISTP](/images/word_cloud_ISTP.png)   [ISFP](/images/word_cloud_ISFP.png)   [INFP](/images/word_cloud_INFP.png)   [INTP](/images/word_cloud_INTP.png)

[ESTP](/images/word_cloud_ESTP.png)   [ESFP](/images/word_cloud_ESFP.png)   [ENFP](/images/word_cloud_ENFP.png)   [ENTP](/images/word_cloud_ENTP.png)

[ESTJ](/images/word_cloud_ESTJ.png)   [ESFJ](/images/word_cloud_ESFJ.png)   [ENFJ](/images/word_cloud_ENFJ.png)   [ENTJ](/images/word_cloud_ENTJ.png)

---
## Summary
- A forum to discuss personality types seems to attract specifc personality types more than others - INxx vs ESxx.
- For posts less than 180 characters long, approximately 50 characters was most common for all types.
- SKLearn is a powerful and easy-to-use tool for document word analysis.
- Some differences can be seen between personality types when viewed as word clouds, but additional text processing would likely yield more clear distinctions.

---
## Future improvements
### Distributions
 - Calculate mean post length for each user, then view as distribution for all means by Type.  Data will likely normally distributed, and a better assessment of post length differences by user can be assessed.

### Word Clouds - lots of pre-processing!
 - Lemmatize (find dictionary root word or variants)
 - Stem (remove suffixes - no guarantee result is a dictionary root word)
 - Additional updates to custom stopword list
 - Review order of processing steps for efficiency
