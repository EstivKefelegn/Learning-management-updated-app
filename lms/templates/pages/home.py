import frappe

def get_context(context):
    try:
        categories = frappe.get_all("LMS Category", fields=["name", "category"])
    except Exception as e:
        frappe.log_error(f"Error fetching categories: {e}", "Home Page Error")
        categories = []
    
    context.categories = categories
    context.title = "Home"
    return context
