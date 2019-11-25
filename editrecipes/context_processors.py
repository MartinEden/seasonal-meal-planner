from django.urls import resolve


class NavItem(object):
    def __init__(self, text, url_name):
        self.text = text
        self.url_name = url_name


static_nav = [
    NavItem('Home', 'index'),
    NavItem('Yearly chart', 'year_chart'),
    NavItem('Tag chart', 'tag_chart'),
    NavItem('Dishes by category', 'all_categories'),
    NavItem('Sidedishes', 'all_sidedishes'),
    NavItem('Plan week', 'plan_week'),
    NavItem('Make a shopping list', 'select_recipes'),
    NavItem('Search by ingredient', 'search'),
    NavItem('Ingredients', 'ingredients')
]


def nav_context(request):
    return {
        'nav': static_nav,
        'current_url_name': resolve(request.path_info).url_name
    }
