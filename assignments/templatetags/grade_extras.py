from django import template
import re

register = template.Library()


@register.filter
def grade_badge_class(grade):
    """Return a bootstrap badge class for a given grade string or numeric value."""
    if not grade:
        return 'secondary'

    g = str(grade).strip()

    # Numeric grade
    try:
        val = float(g)
        if val >= 85:
            return 'success'
        if val >= 70:
            return 'info'
        if val >= 50:
            return 'warning'
        return 'danger'
    except Exception:
        pass

    # Letter grades (A, A-, B+, ...)
    if re.match(r'^[Aa][\+\-]?$|^[Bb][\+\-]?$|^[Cc][\+\-]?$|^[Dd][\+\-]?$|^[Ff]$', g):
        # Map letters to classes
        letter = g[0].upper()
        if letter == 'A':
            return 'success'
        if letter == 'B':
            return 'info'
        if letter == 'C':
            return 'warning'
        return 'danger'

    # Fallback
    return 'secondary'


@register.filter
def grade_display(grade):
    """Normalize grade display: numeric without trailing .0, uppercase letters."""
    if grade is None:
        return ''
    g = str(grade).strip()
    try:
        val = float(g)
        if val.is_integer():
            return str(int(val))
        return str(val)
    except Exception:
        return g.upper()
