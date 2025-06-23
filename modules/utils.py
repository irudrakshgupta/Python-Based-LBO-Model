def format_currency(value):
    """Format a number as currency."""
    if value is None:
        return "N/A"
    return f"${value:,.2f}"

def format_percentage(value):
    """Format a number as percentage."""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"

def neon_palette():
    """Return a list of neon colors for consistent styling."""
    return [
        '#00FFE7',  # Neon Cyan
        '#FF00E7',  # Neon Pink
        '#E7FF00',  # Neon Yellow
        '#00FF38',  # Neon Green
        '#FF3800',  # Neon Red
        '#00B4FF',  # Neon Blue
    ] 