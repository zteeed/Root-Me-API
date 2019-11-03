routes = {
    'info': f'GET /',
    'categories': f'GET /<string:lang>/categories',
    'category_info': f'GET /<string:lang>/category/<string:category>',
    'challenges': f'GET /<string:lang>/challenges',
    'user_profile': f'GET /<string:lang>/<string:username>/profile',
    'user_contributions': f'GET /<string:lang>/<string:username>/contributions',
    'user_created_challenges': f'GET /<string:lang>/<string:username>/contributions/challenges',
    'user_published_solutions': f'GET /<string:lang>/<string:username>/contributions/solutions',
    'user_details': f'GET /<string:lang>/<string:username>/details',
    'user_ctf_all_the_day_data': f'GET /<string:lang>/<string:username>/ctf',
    'user_stats': f'GET /<string:lang>/<string:username>/stats',
}
