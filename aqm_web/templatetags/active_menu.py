from django import template

register = template.Library()

@register.tag
def active(parser, token):
    import re
    args = token.split_contents()
    template_tags = args[0]
    if len(args) < 2 :
        raise template.TemplateSyntaxError, '%s tag requires at least one arguments' % template_tags
    
    return NavSelectedNode(args[1:])

class NavSelectedNode(template.Node):
    def __init__(self, patterns):
        self.patterns = patterns
    
    def render(self, context):
        path = context['request'].path
        for p in self.patterns:
            pval = template.Variable(p).resolve(context)
            if path == pval:
                return 'active'
        return ''

    