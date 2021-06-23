# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ScrapydemoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 书籍信息


class bookItem(Item):
    id = Field()
    status = Field()
    tags = Field()
    shielded = Field()
    defaultSource = Field()
    score = Field()
    scoreDetail1 = Field()
    scoreDetail2 = Field()
    scoreDetail3 = Field()
    scoreDetail4 = Field()
    scoreDetail5 = Field()
    scorerCount = Field()
    commentCount = Field()
    addListCount = Field()
    addListTotal = Field()
    recom_ignore = Field()
    title = Field()
    author = Field()
    cover = Field()
    introduction = Field()
    countWord = Field()
    updateAt = Field()
    v = Field()
    caseId = Field()
    classInfo = Field()
    classId = Field()
    className = Field()
    channel = Field()

# 书源地址


class bookSourceItem(Item):
    bookId = Field()
    siteName = Field()
    bookPage = Field()

# 评论列表


class bookListCommentItem(Item):
    id = Field()
    createrUserId = Field()
    createrUserName = Field()
    content = Field()
    createdAt = Field()
    inReview = Field()
    jurisdiction = Field()
    praiseCount = Field()
    replyCount = Field()
    score = Field()
    shielded = Field()
    tags = Field()
    stickie = Field()
    sortId = Field()
    bookId = Field()
    collected = Field()
    booklistShipId = Field()
    voting = Field()
    replyable = Field()

# 书单信息


class bookListInfoItem(Item):
    id = Field()
    inReview = Field()
    editable = Field()
    comTotal = Field()
    clicks = Field()
    collectNum = Field()
    favsTotal = Field()
    bookTotal = Field()
    praiseTotal = Field()
    essence = Field()
    shielded = Field()
    deleted = Field()
    unSearch = Field()
    createrUserId = Field()
    createrUserName = Field()
    title = Field()
    listType = Field()
    content = Field()
    createdAt = Field()
    updateAt = Field()
    praiseAt = Field()
    v = Field()
    collected = Field()
    voting = Field()

class bookListItem(Item):
    bookListId = Field()
    bookId = Field()
