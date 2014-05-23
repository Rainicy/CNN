# CNN PROJECT

**_This is the project for crawling CNN news articles and comments from Disqus._**

## DICTIONARY DESCRIPTION:

*NOTE: ',' in each Format means '\t' in the file.*

#### 1. Article Tables:

###### 1) Author Table:

        Format: {Author_ID, Author_Name, Author_Title, Article_Counts}

        FilesName: "Dict_Authors"

###### 2) Article Table:

        Format: {Art_ID, Art_Title, Date, URL, Text}

        FileName: "Dict_Articles"

###### 3) Article&Author Relation Table:

        Format: {Author_ID, Art_ID}

        FileName: "Dict_Author_Article"

#### 2. Comments Tables:

    1) Article&Comment Relation Table:

        Format: {Art_ID, Comment_ID}

        FileName: "Dict_Article_Comment"

    2) Comment Table:

        Format: {ID, User_ID, parent(reply_to), createdAt, likes, dislikes, message}

        FileName: "Dict_Comments"

    3) User Table:

        Format: {User_ID, User_Name, Name, joinedAt, reputation}

        FileName: "Dict_Users"

