Authentication System Documentation
1. System Overview
The authentication system is built using the Django Authentication Framework, adhering to the Model-View-Template (MVT) architecture. It utilizes Django's built-in session management and security protocols to handle user identity.

Key Components
Views:

register: A custom view logic handling POST requests for data submission and GET requests for form rendering. Utilizes UserCreationForm extended with email support.

profile: A protected view (using the @login_required decorator) that handles both user data display and updates via UserUpdateForm.

LoginView & LogoutView: Django's class-based views utilized to handle session creation and destruction securely.

Forms:

CustomUserCreationForm: Extends the standard Django form to capture email addresses during sign-up.

UserUpdateForm: A ModelForm linked to the User model, allowing updates to username and email.

Templates: Custom HTML templates (register.html, login.html, profile.html) styled with CSS to provide a user-friendly interface.

2. Security Implementation
The system implements industry-standard security measures automatically via Django:

CSRF Protection: All forms (Login, Register, Update) include a Cross-Site Request Forgery ({% csrf_token %}) token. This prevents malicious sites from submitting data on behalf of a logged-in user.

Password Hashing: Passwords are never stored in plain text. The system uses the PBKDF2 algorithm with a SHA256 hash to encrypt passwords in the PostgreSQL database.

Session Security: User sessions are stored in the database, and session cookies are set with HttpOnly flags to prevent access via JavaScript (XSS mitigation).

3. User Interaction Guide (Testing Instructions)
To verify the authentication system, follow these steps:

Step A: User Registration
Navigate to the registration URL (e.g., /register/).

Fill in the "Join Us" form with a unique username, valid email, and strong password.

Expected Outcome: Upon successful submission, the user is redirected to the Login page.

Step B: Login
Navigate to the login URL (e.g., /login/).

Enter the credentials created in Step A.

Expected Outcome: The user is authenticated, a session is created, and the browser redirects to the User Profile.

Step C: Profile Management
Ensure you are logged in.

Navigate to the Profile page.

Modify the email address field and click "Update".

Expected Outcome: The page reloads, and the new email is persisted in the database.

Step D: Logout & Security
Click the "Logout" button.

Attempt to manually navigate back to the /profile/ URL.

Expected Outcome: The system detects the lack of an active session and automatically redirects the browser back to the Login page.