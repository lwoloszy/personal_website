Title: AlbumPitch: a text based music recommender
Date: 2016-10-24
Tags: NLP, bag-of-words, LSA, MongoDB, SQL
Category: Data science
Slug: albumpitch
Summary: An end-to-end data science project that uses statistical NLP on data scraped from Pitchfork.com to generate album recommendations via an interactive web app
Status: 


Overview
--------
This is a short post describing the capstone project I worked on while a student at Galvanize's Data Science Immersive class. In a nutshell, it is a music recommendation system that relies on text information gleaned from the web. It is a project that tries to capture all three phases of a typical data science product: data collection and storage, data analysis and modeling, and model deployment via a website. If you'd like to cut through the weeds, just visit [AlbumPitch](http://www.albumpitch.com) and start receiving recommendations! If you'd like to learn more about the process of how the project came to be, read on.

---

Motivation
----------
With the advent of online music streaming services like Spotify, Apple Music, Tidal, Pandora and others, we live in an age where it is incredibly easy to access any kind of music. As the average listener’s curiosity and desire for new music has increased, streaming platforms have adopted a combination of human curators and computer algorithms to help create personalized playlists that they believe the listener will enjoy. The vast majority of such playlists consist of individual songs from a mishmash of artists. However, it is in the album format that artists originally intended their music to be listened. Call me a traditionalist, but I am one of those people who prefers the full album experience. So what’s an album-phile like me to do? Well, this past decade has seen numerous dedicated music review sites come into existence. I figured that I could use the semantic content of these reviews to make album suggestions. For this project in particular, I decided to pair [Pitchfork](http://www.pitchfork.com), one of the better known and more consistent  music blogs, with [Spotify](http://www.spotify.com), to create AlbumPitch, an album recommendation engine based solely on text information.

---

Data collection and storage
---------------------------
#### Pitchfork
As with any data science application, this project began with data collection. I scraped the entire Pitchfork site, which at the time had 17833 reviews spanning 9 genres (I've since rescraped it to get a few more reviews). I learned the hard way that the best way to scrape a site is to grab and store all the raw html pages found on the site and only parse them later. Don't try to parse on the fly. This approach has at least two immediate advantages. For one, if a page is missing some information that the parser is expecting, it won't block the script. Second, and perhaps more importantly, if you ever want to extract additional information from the html, you won't have to rescrape the entire site. All the raw html will be there on your local storage device, and all you'll have to do is reparse. Trust me, much faster this way. To store the scraped data, I ended up using MongoDB, in part to learn how to work with it and in part because it was super convenient for storing the sorts of documents found on Pitchfork. The script for scraping Pitchfork can be found [here](https://github.com/lwoloszy/albumpitch/blob/master/src/scrapers/pitchfork_scraper.py) and the script for parsing that information can be found [here](https://github.com/lwoloszy/albumpitch/blob/master/src/parse_reviews.py).

Some basic exploratory graphs summarizing the review meta-information are shown below. As you can see, Pitchfork has fairly long-form reviews (partly the reason I chose to use this particular site), containing a mixture of information relevant to generating recommendations, such as nuanced descriptions of the various genres and tempos present in the album, other artists the album was influenced by, and the overall sentiment of the reviewer towards the album.

**_Figure 1: Basic descriptive statistics of reviews scraped from Pitchfork._**

Genre distribution         |  # of reviews by reviewer | Review length distribution
:-------------------------:|:-------------------------:|:-------------------------:
<img src="{filename}/images/2-genre_dist.png" style="width: 275px;"/> | <img src="{filename}/images/2-reviewer_dist.png" style="width: 275px;"/> | <img src="{filename}/images/2-review_length_dist.png" style="width: 275px;"/>



#### Spotify API
In addition to scraping the Pitchfork site, I wanted to run some validation tests (see below) that required me to use Spotify's audio features API call. This was a multistage process where I first tried to find the album id in the Spotify catalog corresponding to the Pitchfork album whose audio features I was interested in, then I would find all the track ids for that album, and finally I would retrieve the audio features for each and every track id. Oftentimes, the call to Spotify to find an album id would result in multiple albums being returned. I needed to find the best correspondence between the Pitchfork album that seeded the query and one of the albums returned by Spotify, if any. To run this co-registration process, which relied on several carefully handcrafted heuristics that you might want to play around with, look at the ```coregister_albums``` function [here](https://github.com/lwoloszy/albumpitch/blob/master/src/spotify.py). I'm not guaranteeing that this matching process is perfect, as naturally there will be some false positives and false negatives, but I would say it's within 1-3% of what's achievable. Also, Spotify's catalog, while immense, is far from complete with respect to albums that Pitchfork has reviewed.

#### PostgreSQL transfer
Ultimately, to put the Spotify and Pitchfork data into a more quickly manipulable format, a format that was also directly transferable to Heroku, I put all this data into a PostgreSQL database. 

---

## Data analysis and modeling
#### Primary models
My two main tools for generating album recommendation from text data were Latent Semantic Analysis (LSA) and Latent Dirichlet Allocation (LDA), two algorithms famous for discovering hidden topics within a corpus of documents. Figure 2 outlines how I used LSA to make recommendations, which amounted to finding albums whose reviews were similar semantically to the album seeding the query. I found from listening to A LOT of sample recommendations that in general LSA seemed to work better than LDA, so that's the method I stuck with. However, the bulk of my time to get either tool to work reasonably well was spent devising various regular expressions to capture some of the idiosyncrasies of music reviews, which, naturally, included a lot of references to artists, bands and albums, which are multi-token patterns that would get lost in the simplest of bag-of-words approach. This [file](https://github.com/lwoloszy/albumpitch/blob/master/src/text_preprocess.py) contains most of the regular expressions. One of my other breakthroughs in LSA was using sublinear scaling on the TF term, which helped counteract the sometimes numerous mentions of one artist in a single review, and thus increased the relative importance of some of the more descriptive words.

**_Figure 2: Latent Semantic Analysis applied to text reviews can be used to generate album recommendations._**
*We begin by decomposing each review into its constituent words, and then, through a series of transformations (tf-idf scaling followed by the dimension-reducing Singular Value Decomposition), we can obtain, for each review, its low dimensional vector space representation. With these vectors in hand, generating recommendations is almost trivial. We just take the review of some album we like, and find albums whose reviews are similar using some metric like cosine similarity.*
![]({filename}/images/2-lsa.png)

#### Validation
As I mentioned, earballing the recommendations was the primary means by which I evaluated the models, but I did have a few heuristics I used to gauge how well LSA was doing. For one, I visualized A LOT (again) of the hidden dimensions that LSA would produce, seeing whether they were capturing words relevant to discriminating various genres of music (where relevant was based on my own personal experience reading music reviews). One such plot is shown below. As you can see, many of the terms do cluster along obvious genres such as rock, rap, electronic and acoustic (though it should be acknowledged that many terms are also less obviously related to music per se). Also note that I've applied the snowball stemmer to the words, which is why many of them have what appear to be missing suffixes.

**_Figure 3: Top 10 LSA components from a model with 200 dimensions._** 
*Each subplot shows a single hidden component discovered by LSA, with the 6 words having the heighest weight shown in red and the 6 words having the lowest weight shown in blue.*
![]({filename}/images/2-svd.png)

We can go one step further and look at the clusters that k-means algorithm gives us when applied to data that has been transformed with LSA. Again, these seemed to make quite a bit of sense, reassuring me that the LSA approach in general was working.

**_Figure 4: 10 random clusters discovered by k-means algorithm (clustering was done in the LSA space)._** 
*Each subplot shows a single k-means cluster, with the 12 words having the heighest weight shown.*
![]({filename}/images/2-kmeans.png)

However, some form of external validation would be better. For this, I turned to the audio features that I got from Spotify (via Echonest). As background, Spotify has quantified a large collection of songs along a number of subjective features, such as acousticness, danceability, energy, loudness and so on. I hypothesized that if my recommendations were making any sense, then the further down the recommendation list we go, the more dissimilar these albums should be to the album that initiated the query. Indeed, in the figure below, you can see that this monotonic increase in audio dissimilarity as a function of recommendation rank is present for all audio features examined, suggesting that the semantic content of music reviews has, to some degree, a relationship with audio features.

**_Figure 5: Audio feature differences between a seed album and a recommended album._** 
*Audio differences are plotted as a function of recommendation rank. All the y-axis labels should have the word "difference" added to them, but for clarity, those have been omitted.*
![]({filename}/images/2-individual_afs.png)

---

## Web app deployment
I deployed the final LSA-based recommendation system via a basic web app that you can explore [here](http://www.albumpitch.com). This app will produce, given either a seed album or a keyword search, a list of albums you might enjoy. A screenshot is provided below. It's not perfect by any means, as there are numerous improvements that could be made to the model, but in many instances it gives reasonable suggestions. Keep in mind, these recommendations are based solely on text information, so they're unlikely to be perfect. It really is a fun tool to play with! I've already found a few new albums through it that I like.

![]({filename}/images/2-albumpitch.png)

---

## Future directions
One of the most obvious next steps for this project would be to incorporate a Named Entity Recognition (NER) system that would allow for better identification of artist, band, album and song mentions within a piece of text. As I alluded to, I had to do quite a lot of regular expression magic to format the review data in such a way that its relevant features were consumable by the bag-of-words model, but this approach definitely fell short of what's achievable with a state-of-the-art NER. 

Another point of improvement for AlbumPitch would be better attribution of the various parts of the review to the relevant entity/concept. Oftentimes, a reviewer would compare the album that was the subject of the review to another album, and then spend a significant part of the review talking about how that other album was different, and of course that's all relevant information for making recommendations but also information that gets completely lost when we decompose the review into its constituent words. Along similar lines, it would be interesting to see whether dealing with sentences that contained words with strong sentiment association would provide more objective searches, independent of the reviewer's own bias. I guess this all depends on the intent of the application.

Ideally, I'd also have designed the web app in such a way that it would automatically scrape new Pitchfork reviews every day, and then incorporate those reviews into its database of potential recommendations. As it stands, I have to do this manually, which is not really realistic on a daily basis. Given that I do find this tool helpful, I may periodically update the site every few months, but only time will tell how consistent I am about this. (Honestly, I think Pitchfork would find this tool pretty cool too, but I have yet to share this project with them...)

Last, I would love to do an experiment to see whether the semantic information I'm using to generate album suggestions could help improve recommendation systems that rely on a purely collaborative filtering approach. Spotify, you out there?
