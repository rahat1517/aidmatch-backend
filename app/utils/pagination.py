def paginate(query, page: int = 1, page_size: int = 10):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()