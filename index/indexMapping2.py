indexMapping = {
    "properties" : {
        "id" : {
            "type" : "long"
        },
        "title" : {
            "type" : "text"
        },
        "title_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "author" : {
            "type" : "text"
        },
        "author_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "is_adult" : {
            "type" : "text"
        },
        "is_adult_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "view_count" : {
            "type" : "long"
        },
        "view_count_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "favorite_count" : {
            "type" : "long"
        },
        "favorite_count_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "state" : {
            "type" : "text"
        },
        "state_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "day" : {
            "type" : "text"
        },
        "day_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "platform" : {
            "type" : "text"
        },     
        "platform_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },     
        "genre" : {
            "type" : "text"
        },
        "genre_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "star_score" : {
            "type" : "float"
        },     
        "star_score_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "epi_cnt" : {
            "type" : "long"
        },
        "epi_cnt_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
        "story" : {
            "type" : "text"
        },
        "story_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },          
        "image_url" : {
            "type" : "text"
        },
        "index" : {
            "type" : "long"
        }, 
        "info" : {
            "type" : "text"
        }, 
        "info_vector" : {
            "type" : "dense_vector",
            "dims" : 1536,
            "index" : True,
            "similarity" : "cosine"
        },
    }
}