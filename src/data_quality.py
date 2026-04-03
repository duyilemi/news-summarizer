# def validate_article(article):
#     """Return True if article passes quality checks, else False."""
#     title = article.get('title')
#     url = article.get('url')
#     published_at = article.get('publishedAt')
#     if not title or not url or not published_at:
#         return False
#     if len(title) < 5:
#         return False
#     # Add more checks as needed
#     return True

# def filter_articles(articles):
#     """Return only valid articles."""
#     return [a for a in articles if validate_article(a)]

def validate_article(article):
    """Return True if article passes basic quality checks."""
    title = article.get('title')
    url = article.get('url')
    published_at = article.get('publishedAt')
    # Title must exist and be longer than 5 characters
    if not title or len(title) < 5:
        return False
    # URL must exist
    if not url:
        return False
    # Published date must exist
    if not published_at:
        return False
    return True

def filter_articles(articles):
    """Return only valid articles."""
    return [a for a in articles if validate_article(a)]