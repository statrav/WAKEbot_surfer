indexMapping = {
    "properties" : {
        "id" : {
            "type" : "long"
        },
        "title" : {
            "type" : "text"
        },
        "author" : {
            "type" : "text"
        },
        "is_adult" : {
            "type" : "text"
        },
        "view_count" : {
            "type" : "long"
        },
        "favorite_count" : {
            "type" : "long"
        },
        "state" : {
            "type" : "text"
        },
        "day" : {
            "type" : "text"
        },
        "platform" : {
            "type" : "text"
        },       
        "genre" : {
            "type" : "text"
        },
        "star_score" : {
            "type" : "float"
        },     
        "epi_cnt" : {
            "type" : "long"
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