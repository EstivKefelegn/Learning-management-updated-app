import frappe
from frappe.utils import get_url

def notify_users_on_new_course(doc, method):
    """Send email to all active users when a new course is added"""
    try:
        course_title = doc.title
        course_link = get_url(f"/lms/courses/{doc.name}")
        
        # Use default outgoing email if sender is blank
        sender = None

        # Get all enabled users except Guest
        users = frappe.get_all("User", filters={"enabled": 1}, fields=["email"])
        recipient_emails = [u.email for u in users if u.email and u.email != "guest@example.com"]

        frappe.logger().info(f"[Course Notification] Course '{course_title}' created. Recipients: {recipient_emails}")

        if not recipient_emails:
            frappe.logger().warning(f"[Course Notification] No recipients for course '{course_title}'")
            return

        subject = f"New Course Added: {course_title}"
        message = f"""
        <p>Hello,</p>
        <p>A new course <b>{course_title}</b> has just been uploaded to the LMS.</p>
        <p>Check it out: <a href="{course_link}">{course_link}</a></p>
        <br>
        <p>Best regards,<br>Your LMS Team</p>
        """

        frappe.sendmail(
            recipients=recipient_emails,
            sender=sender,          # None means use Default Outgoing Email
            subject=subject,
            message=message,
            delayed=False
        )

        frappe.logger().info(f"[Course Notification] Email sent for course '{course_title}' to {len(recipient_emails)} users.")

    except Exception as e:
        frappe.logger().error(f"[Course Notification] Error sending email for '{doc.name}': {str(e)}")


# import frappe

# def notify_users_on_new_course(doc, method):
#     """Send email to all active users when a new course is added"""
#     course_title = doc.title
#     course_link = frappe.utils.get_url(f"/lms/courses/{doc.name}")
#     sender = frappe.session.user or "Administrator"

#     # Get all users except Guest
#     users = frappe.get_all("User", filters={"enabled": 1}, fields=["email"])
#     recipient_emails = [u.email for u in users if u.email and u.email != "guest@example.com"]

#     if not recipient_emails:
#         frappe.logger().info("No recipients found for course notification.")
#         return

#     subject = f"New Course Added: {course_title}"
#     message = f"""
#     <p>Hello,</p>
#     <p>A new course <b>{course_title}</b> has just been uploaded to the LMS.</p>
#     <p>You can check it out here: <a href="{course_link}">{course_link}</a></p>
#     <br>
#     <p>Best regards,<br>Your LMS Team</p>
#     """

#     # Send the email
#     frappe.sendmail(
#         recipients=recipient_emails,
#         sender=sender,
#         subject=subject,
#         message=message,
#         delayed=False  # Set to True if you want to queue it for later sending
#     )

#     frappe.logger().info(f"Sent new course notification for '{course_title}' to {len(recipient_emails)} users.")
