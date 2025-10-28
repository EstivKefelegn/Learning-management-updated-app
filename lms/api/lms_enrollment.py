import frappe

def notify_admin_on_enrollment(doc, method):
    """Send email to admin when a student enrolls in a course"""

    # Get course info
    course_title = frappe.db.get_value("LMS Course", doc.course, "title")
    course_link = frappe.utils.get_url(f"/lms/courses/{doc.course}")

    # Get student info
    student_name = doc.student_name or doc.student
    student_email = frappe.db.get_value("User", doc.student, "email")

    # Get admin users (System Managers)
    admin_users = frappe.get_all(
        "Has Role",
        filters={"role": "System Manager"},
        fields=["parent"]
    )
    admin_emails = [
        frappe.db.get_value("User", a.parent, "email")
        for a in admin_users if frappe.db.get_value("User", a.parent, "email")
    ]

    if not admin_emails:
        frappe.logger().info("No admin email addresses found for enrollment notification.")
        return

    # Sender email (domain email)
    sender = frappe.db.get_single_value("Email Account", "default_outgoing") or "noreply@yourdomain.com"

    # Subject & Message
    subject = f"New Enrollment: {student_name} enrolled in {course_title}"
    message = f"""
    <p>Hello Admin,</p>
    <p><b>{student_name}</b> ({student_email}) has enrolled in the course <b>{course_title}</b>.</p>
    <p>You can view the course here: <a href="{course_link}">{course_link}</a></p>
    <br>
    <p>Best regards,<br>Your LMS System</p>
    """

    # Send the email
    frappe.sendmail(
        recipients=admin_emails,
        sender=sender,
        subject=subject,
        message=message,
        delayed=False,
    )

    frappe.logger().info(f"Enrollment notification sent to admins for course {course_title}")
