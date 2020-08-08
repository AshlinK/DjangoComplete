from django import template
from poll.models import Question
register=template.Library()

def upper(value):
    return value.upper()

register.filter('upper',upper)

@register.simple_tag()
def recent_polls(n=5):
    """Return recent n polls."""
    questions=Question.objects.all().order_by('-created_at')[0:n]
    return questions