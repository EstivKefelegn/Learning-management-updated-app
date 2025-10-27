import frappe
from frappe import _
import re

no_cache = 1

def get_context(context):
    # Get course name from URL parameters
    course_name = frappe.form_dict.get("course_id") or frappe.form_dict.get("course")
    
    if not course_name:
        frappe.local.flags.redirect_location = "/courses"
        raise frappe.Redirect
    
    course = frappe.get_doc("LMS Course", course_name)
    context.course = course
    
    # -----------------------------
    # Check if user is enrolled
    # -----------------------------
    context.is_enrolled = False
    context.enrollment_name = None
    if frappe.session.user != "Guest":
        enrollment = frappe.db.get_value("LMS Enrollment",
            {"course": course_name, "member": frappe.session.user},
            "name"
        )
        if enrollment:
            context.is_enrolled = True
            context.enrollment_name = enrollment
    
    # -----------------------------
    # Extract YouTube ID if video_link exists
    # -----------------------------
    if course.video_link:
        context.youtube_id = extract_youtube_id(course.video_link)
    
    # -----------------------------
    # Course stats
    # -----------------------------
    context.enrollments = course.enrollments or 0
    context.lessons_count = course.lessons or 0
    context.rating = course.rating or 0
    
    # Chapters and lessons
    context.chapters = get_course_chapters(course_name)
    
    # Instructors
    context.instructors = get_course_instructors(course.instructors) if course.instructors else []
    
    # Related courses
    context.related_courses = get_related_courses(course.related_courses) if course.related_courses else []
    
    # Meta tags
    context.meta_tags = {
        "title": course.title,
        "description": course.short_introduction or course.description,
        "image": course.image,
        "keywords": course.tags or ""
    }
    
    return context    
    
# -----------------------------
# Helper functions
# -----------------------------

def extract_youtube_id(url):
    """Extract YouTube ID from various YouTube URL formats"""
    if not url:
        return None
    if len(url) == 11 and not any(char in url for char in ['/', '?', '=', '&']):
        return url
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&]+)',
        r'youtube\.com\/embed\/([^?]+)',
        r'youtube\.com\/v\/([^?]+)',
        r'v=([^&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_course_chapters(course_name):
    try:
        if not frappe.db.exists("DocType", "Course Chapter"):
            return []
        chapters = frappe.get_all("Course Chapter",
            filters={"course": course_name},
            fields=["name", "title", "description"],
            order_by="idx"
        )
        for chapter in chapters:
            if frappe.db.exists("DocType", "Course Lesson"):
                chapter.lessons = frappe.get_all("Course Lesson",
                    filters={"chapter": chapter.name},
                    fields=["name", "title", "duration", "content_type", "idx"],
                    order_by="idx"
                )
            else:
                chapter.lessons = []
        return chapters
    except Exception as e:
        frappe.log_error(f"Error getting chapters for course {course_name}: {str(e)}")
        return []

def get_course_instructors(instructors):
    instructor_details = []
    for instructor in instructors:
        try:
            instructor_doc = frappe.get_doc("User", instructor.instructor)
            instructor_details.append({
                "name": instructor_doc.name,
                "full_name": instructor_doc.full_name,
                "bio": getattr(instructor_doc, 'bio', ''),
                "headline": getattr(instructor_doc, 'headline', 'Course Instructor'),
                "user_image": instructor_doc.user_image
            })
        except Exception as e:
            frappe.log_error(f"Error getting instructor details: {str(e)}")
            continue
    return instructor_details

def get_related_courses(related_courses):
    related = []
    for related_course in related_courses:
        try:
            course = frappe.get_doc("LMS Course", related_course.course)
            if course.published:
                related.append({
                    "name": course.name,
                    "title": course.title,
                    "image": course.image,
                    "short_introduction": course.short_introduction,
                    "course_price": course.course_price,
                    "currency": course.currency
                })
        except Exception as e:
            frappe.log_error(f"Error getting related course: {str(e)}")
            continue
    return related[:3]

# -----------------------------
# Invoice generation
# -----------------------------
@frappe.whitelist()
def generate_course_invoice(enrollment_name):
    """
    Generate invoice data from LMS Payment for course enrollment.
    This uses LMS Payment data directly, not Sales Invoice.
    """
    try:
        frappe.logger().info(f"🔍 Looking for payment data for enrollment: {enrollment_name}")

        # Get enrollment details
        if not frappe.db.exists("LMS Enrollment", enrollment_name):
            return {
                "success": False,
                "error": "Enrollment not found."
            }

        enrollment = frappe.get_doc("LMS Enrollment", enrollment_name)
        
        if not enrollment.payment:
            return {
                "success": False,
                "error": "No payment record found for this enrollment."
            }

        # Get payment details
        payment = frappe.get_doc("LMS Payment", enrollment.payment)
        
        if not payment.payment_received:
            return {
                "success": False,
                "error": "Payment not completed. Cannot generate invoice."
            }

        # Get course details
        course = frappe.get_doc("LMS Course", enrollment.course)
        
        # Get address details if available
        address_details = {}
        if payment.address:
            try:
                address_doc = frappe.get_doc("Address", payment.address)
                address_details = {
                    "address": address_doc.display(),
                    "gstin": address_doc.gstin,
                    "pan": getattr(address_doc, 'tax_id', None) or getattr(address_doc, 'pan', None)
                }
            except Exception:
                address_details = {}

        # Prepare invoice data from LMS Payment
        invoice_data = {
            "number": payment.name,  # Use payment name as invoice number
            "date": payment.creation.date(),
            "due_date": payment.creation.date(),  # Same as creation date for paid invoices
            "status": "Paid",
            "currency": payment.currency,
            "total_amount": payment.amount,
            "amount": payment.amount,  # Net amount (same as total for simplicity)
            "tax_amount": 0,  # You can calculate this if you have tax details
            "course_title": course.title,
            "customer": payment.member,
            "billing_name": payment.billing_name,
            "payment_reference": payment.payment_id or payment.order_id,
            "order_id": payment.order_id,
            "payment_id": payment.payment_id,
            "gstin": payment.gstin,
            "pan": payment.pan
        }

        # Add address details
        invoice_data.update(address_details)

        return {
            "success": True,
            "message": "Payment invoice generated successfully",
            "invoice_data": invoice_data
        }
            
    except Exception as e:
        frappe.log_error(message=f"Payment Invoice Error: {str(e)}", title="Payment Invoice Generation")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_sales_invoice(enrollment_name):
    """
    Fetch payment invoice data for this enrollment.
    """
    try:
        # Check for enrollment and payment
        if not frappe.db.exists("LMS Enrollment", enrollment_name):
            return {
                "success": False,
                "message": "Enrollment not found."
            }

        enrollment = frappe.get_doc("LMS Enrollment", enrollment_name)
        
        if not enrollment.payment:
            return {
                "success": False,
                "message": "No payment record found for this enrollment."
            }

        payment = frappe.get_doc("LMS Payment", enrollment.payment)
        
        return {
            "success": True,
            "invoice_name": payment.name,
            "status": "Paid" if payment.payment_received else "Unpaid",
            "currency": payment.currency,
            "total": payment.amount,
            "message": "Payment invoice found successfully."
        }

    except Exception as e:
        frappe.log_error(str(e), "Get Payment Invoice Error")
        return {"success": False, "error": str(e)}

def create_valid_address(customer):
    """Create a properly formatted address with all required fields"""
    try:
        # Check if address already exists for this customer
        existing_address = frappe.db.get_value("Address", 
            {"address_title": f"{customer} - Billing Address"}, "name")
        if existing_address:
            return existing_address
            
        # Create new address with all required fields
        address_doc = frappe.get_doc({
            "doctype": "Address",
            "address_title": f"{customer} - Billing Address",
            "address_type": "Billing",
            "address_line1": "Online Course Purchase",
            "city": "Mumbai",
            "state": "Maharashtra", 
            "country": "India",
            "pincode": "400001",
            "is_primary_address": 1,
            "is_shipping_address": 1,
        })
        
        # Add link properly using append method
        address_doc.append("links", {
            "link_doctype": "Customer",
            "link_name": customer
        })
        
        address_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return address_doc.name
        
    except Exception as e:
        frappe.log_error(f"Address creation failed: {str(e)}")
        # If address creation fails, try to use any existing address
        fallback_address = frappe.db.get_value("Address", 
            {"links.link_doctype": "Customer", "links.link_name": customer}, "name")
        if fallback_address:
            return fallback_address
            
        # Last resort: use any address in the system
        any_address = frappe.db.get_value("Address", {}, "name")
        return any_address

def get_invoice_data(invoice):
    """Extract invoice data for frontend display"""
    course_title = frappe.get_value("LMS Course", invoice.course, "title") if invoice.course else "Unknown Course"
    
    return {
        "number": invoice.invoice_number,
        "name": invoice.name,
        "date": invoice.invoice_date,
        "due_date": invoice.due_date,
        "customer": invoice.customer,
        "billing_name": invoice.billing_name,
        "course": invoice.course,
        "course_title": course_title,
        "amount": invoice.amount or 0,
        "total_amount": invoice.total_amount or 0,
        "tax_amount": invoice.tax_amount or 0,
        "currency": invoice.currency or "INR",
        "status": invoice.status or "Unpaid",
        "payment_reference": invoice.payment_reference,
        "payment_for": invoice.payment_for,
        "address": invoice.address,
        "gstin": invoice.gstin,
        "pan": invoice.pan
    }
