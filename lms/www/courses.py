import frappe

def get_context(context):
    # Get category slug from the URL
    category_slug = frappe.form_dict.category

    # Convert slug (e.g. "digital_marketing") → readable name ("Digital Marketing")
    category_name = category_slug.replace("_", " ").title()

    # Check if category exists
    category_exists = frappe.db.exists("LMS Category", {"category": category_name})
    context.selected_category = category_name if category_exists else "Unknown Category"
    context.title = context.selected_category

    # Fetch courses under this category
    courses = frappe.get_all(
        "LMS Course",
        filters={"category": category_name, "published": 1},
        fields=["name", "title", "short_introduction", "image", "course_price", "currency"]
    )

    # Attach currency symbol to each course
    for course in courses:
        if course.currency:
            symbol = frappe.db.get_value("Currency", course.currency, "symbol")
            course.currency_symbol = symbol or course.currency
        else:
            course.currency_symbol = ""

    context.courses = courses
    return context
