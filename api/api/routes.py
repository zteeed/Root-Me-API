from api.constants import VERSION

routes = {
    'info': f'GET /{VERSION}',
    'categories': f'GET /{VERSION}/categories',
    'category_info': f'GET /{VERSION}/category/<string:category>',
    'challenges': f'GET /{VERSION}/challenges',
    'user_profile': f'GET /{VERSION}/<string:username>/profile',
    'user_contributions': f'GET /{VERSION}/<string:username>/contributions',
    'user_created_challenges': f'GET /{VERSION}/<string:username>/contributions/challenges',
    'user_published_solutions': f'GET /{VERSION}/<string:username>/contributions/solutions',
    'user_details': f'GET /{VERSION}/<string:username>/details',
    'user_ctf_all_the_day_data': f'GET /{VERSION}/<string:username>/ctf',
    'user_stats': f'GET /{VERSION}/<string:username>/stats',
}
