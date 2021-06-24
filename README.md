# Recursive deck generation algorithm based on Rank Biserial Correlation

This program builds two lists out of a list of scores such that lists satisfy a desired rank biserial correlation (RBSC) relation [1]. The implementation is done in Python 3.5.2 with no specific dependencies.

Note that this repository addresses a hypothetical case, where the scores array is a set of pseudo-random integers. In practice, depending on  the application, one may use as list of scores number of Google search results [2,3,4], number of occurrences of words in a corpus [4] etc. Since a generic hypothetical case is addressed, the program does not yield the two decks themselves but the lists of scores of the cards in those decks. One may simply map the scores back to the cards (i.e. words) in order to contrusct the decks. 

The algorithm relies on the fact that by adding and removing a single score at a time, the relation between two lists converge to the desired value of RBSC [6]. For composing the decks, two requirements are posed as uniformity and diversity. Uniformity implies that the difficulty level of the cards in the same deck needs to be uniform enough so that they can be grouped together. The diversity requirement poses that the difficulty levels of the cards in different decks need to be diverse enough so that they can be grouped in different decks. The RBSC is used to assess the levels of uniformity and diversity and an iterative algorithm makes the RBSC converge to the desired level.


**References**

[1] Dave S. Kerby, "The simple difference formula: An approach to teaching nonparametric correlation.", Comprehensive Psychology 3 (2014): 11-IT.

[2] Sakthithasan Sripirakas, GoogleSearch, https://github.com/sripirakas/GoogleSearch

[3] Anthony Hseb, googlesearch, https://github.com/anthonyhseb/googlesearch

[4] Zeynep Yücel, Batch searching/logging in Google news in Japanese, https://github.com/yucelzeynep/Batch-search-in-Google-news-in-Japanese

[5] Wiktionary: Frequency lists, https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists

[6] Zeynep Yücel, et al. "An algorithm for automatic collation of vocabulary decks based on word frequency." IEICE Transactions on Information and Systems 103.8 (2020): 1865-1874.
