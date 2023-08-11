# e-Mail
#### Description:
This is a small email like web application. In order to interact with a SQLite database, it makes use of the CS50 library and includes numerous routes for a variety of functionalities, including email composing and sending, managing the bin (deleted emails), logging in and out, registering new users, and responding to emails. The Flask application is set up, the routes are defined, and HTML templates for rendering the web pages are included in the code. The code likewise imports different modules and assistant capabilities to help the application's usefulness.
Lets start with the "app.py":

The code imports the necessary modules and functions from a variety of libraries, including os, cs50, flask, and others, to begin with. The email management system needs these modules to function properly.
An instance of the Flask class is initialized and assigned to the variable app to create the Flask application.
The usd custom filter is associated with the Flask application's Jinja environment. The output of template variables can be altered with the help of custom filters.
The session configuration is set to store session data on the filesystem. Instead of using signed cookies, this configuration enables the application to store session data on the server's filesystem.
The SQL class from the cs50 module is used to establish a connection to the SQLite database. Project.db is the database file utilized.
A function that modifies the response headers to prevent webpage caching is defined with the after_request decorator. This makes sure that the most recent content is always shown.
The main course decorator @app.route("/") characterizes the way of behaving of the application when the client visits the root URL ("/"). The login_required decorator guarantees that the client should be signed in to get to this course. The logged-in user's received emails are retrieved and displayed using the inbox() function.
The behavior of the "/compose" URL is set by the second route decorator, @app.route("/compose", methods=["GET", "POST"]). This course permits the client to compose another email. Both GET and POST requests are handled by compose(). For GET demands, it delivers the "compose.html" layout, passing the username of the source. It inserts a new email record into the database and retrieves the form data (sender, recipient, subject, and body) for POST requests.
The behavior of the "/sent" URL is defined by the third route decorator, @app.route("/sent"). This course shows the sent messages for the signed in client. The capability sent() brings and delivers the sent messages utilizing the "index.html" format.
The behavior of the "/bin" URL is specified by the fourth route decorator, @app.route("/bin", methods=["GET", "POST"]). Emails can be moved to the trash without being deleted using this method. For POST demands, it refreshes the "erased" segment of the comparing email record in the data set. For GET demands, it brings and delivers the messages that are in the receptacle utilizing the "bin.html" layout.
The "/delete" URL's behavior is specified by the fifth route decorator, @app.route("/delete", methods=["POST"]). This course handles the erasure of an email. It displays the details of the email to be deleted in the "delete_confirm.html" template and retrieves the email ID from the form data.
The 6th course decorator @app.route("/erase affirm", methods=["POST"]) characterizes the way of behaving for the "/erase affirm" URL. This course handles the affirmation of email erasure. The email record is removed from the database if the confirmation indicates "yes."
The seventh course decorator @app.route("/reestablish", methods=["POST"]) characterizes the way of behaving for the "/reestablish" URL. The restoration of a deleted email is handled by this route. It recovers the email ID from the structure information and renders the "restore_confirm.html" format, showing the subtleties of the email to be reestablished.
The behavior of the "/restore-confirm" URL is specified by the eighth route decorator, @app.route("/restore-confirm", methods=["POST"]). This course handles the affirmation of email rebuilding. The database's "deleted" column for the email record is updated if the confirmation is "yes."
The "/login" URL's behavior is specified by the ninth route decorator, @app.route("/login", methods=["GET", "POST"]). This course handles client login usefulness. For GET demands, it delivers the "login.html" layout. For POST demands, it recovers the submitted username and secret key, inquiries the data set to approve the accreditations, and sets the "user_id" meeting variable upon fruitful login.
The 10th course decorator @app.route("/logout") characterizes the way of behaving for the "/logout" URL. By rerouting the user to the login form and clearing the session variable "user_id," this route logs the user out.
The "/email" URL's behavior is set by the eleventh route decorator, @app.route("/email", methods=["POST"]). This course recovers the email ID from the structure information and renders the "email.html" layout, showing the subtleties of the chose email.
Regular expressions are supported by importing the re module. It is utilized later for email approval.
The behavior of the "/register" URL is set by the twelfth route decorator, @app.route("/register", methods=["GET", "POST"]). This course handles client enrollment usefulness. For GET demands, it delivers the "register.html" layout. For POST demands, it recovers the submitted email, secret key, and affirmation, approves the information, embeds another client record into the data set, and sets the "user_id" meeting variable upon effective enlistment.
The behavior of the "/reply" URL is specified by the thirteenth route decorator, @app.route("/reply", methods=["GET", "POST"]). This course permits the client to answer to an email. It displays the details of the email to be replied to in the "reply.html" template and retrieves the email ID from the form data.

The "helpers.py" Has not been changed, it is used like the problem set week #9

Now the html sections that have been implemented:
All of the hmtl's begin with "% extends "layout.html" %, indicating that it extends the "layout.html" HTML template. This permits the ongoing format to acquire the design and blocks characterized in the "layout.html" layout. The {% block title %} and {% endblock %} labels characterize the title of the page, which will be shown in the program's title bar. For evry html the title is changed for what its suppsoed to do.The {% block primary %} and {% endblock %} labels characterize the fundamental substance of the page. The parent template's "layout.html" corresponding block will contain everything in between these tags.In every html the page's background color is set to a light yellowish color (#FFFAD7) by using the body> tag.

Bin.html(Displays emails moved to the trash bin) -
Inside the fundamental block, there is a <h1> heading label that shows the text "Bin" with a particular style.
The substance is enveloped by a <div> component with the class "table-responsive". If the table inside it fills the screen, this class makes it possible to scroll horizontally.
A table structure for displaying the email data is defined by the <table> element.
The column titles for the table header row are in the <thead> section. "Sender," "Recipient," "Subject," "Restore," and "Delete".
The table body, which houses the actual email data, can be found in the tbody> section. It utilizes a for circle to emphasize over each email in the "messages" list.
A new table row <tr> is created for each email, and individual table cells <td> display the sender, recipient, and subject.
The last two cells contain the "Restore" and "Delete" buttons. When clicked, they send a POST request to the respective routes (/restore and /delete) with the corresponding email ID as a hidden input value. They are enclosed in their own form> elements.

Compose.html(place to create email and send them out to other users) -
The substance is enveloped by a <form> component that sends a POST solicitation to the "/form" course when submitted.
There are a number of <div> elements inside the form that represent various components of the compose form.
The "From:" label can be found in the first <div> and an area where the sender's email address can be entered. When the page loads, the autofocus attribute makes sure that the input field is automatically focused. The initial value of the input field is set by the value="sender" attribute to the value of the "sender" variable.
The second <div> contains a name "To:" and an area where the recipient's email address can be entered.
The third <div> contains a name "Subject:" furthermore, an information field for the email subject.
A <textarea> element for entering the email's body text is contained in the fourth <div>. The name of the field that will be sent when the form is submitted is specified by the name="body" attribute.
Last but not least, the "Send" button is a <button> element of the class "button-send." When clicked, it sets off the structure accommodation.

Delete_confirmation.html(displays confirmation message for deleting an email) -
The heading "Delete e-Mail" is displayed in the <h1> tag.
The substance is enveloped by a <form> component that sends a POST solicitation to the "/delete-confirm" course when submitted.
Inside the structure, there is a <input> field with the sort "hidden". The value of the email ID that needs to be deleted is stored in it. The name of the field is specified by the name="emailId" attribute, and the value of the field is set by the value="emailDetail.id" attribute to the ID of the email that needs to be deleted.
The message "Are you sure you want to delete this email?" is displayed in the <p> tag to affirm the erasure.
Two "<button>" elements exist: one with the label "Yes" and the class "button-Move," and the other with the label "No" and the class "button-View." The confirmation or cancellation of the deletion can be done through these buttons. They send a POST request to the "/delete-confirm" route with the appropriate confirmation value (either "yes" or "no" for the confirmation field) when clicked, triggering the submission of the form.

email.html(displaying the details and adding the reply method) - The substance is enclosed by a <div> component with the class "center-div". This div is utilized to focus adjust the substance on the page.
There are a number of <div> elements with the class "list-group-item view-email" contained within the div. The sender, recipient, subject, timestamp, and text of the email are all displayed in these divs, which also represent various parts of the email.
A label and a <strong> tag are used to display each information section. For instance, the source data is shown as "Sender: {{ emailDetail.sender }}", where emailDetail.sender is a variable that holds the sender's incentive for the particular email being seen.
A <div> element with the class "my-3" adds some margin space below the email content.
There is a <form> element within this div that, when submitted, sends a POST request to the "reply" route.
The email ID (emailDetail.id) that is currently being viewed can be stored in the form's "hidden" <input> field. A hidden field with the name "emailId" contains this value and is sent to the "reply" route.
A <button> element has the label "Reply" and the class "button-send." When clicked, the form is submitted and a POST request is sent to the "reply" route.

index.html( content for the "emails" page, displaying a table of emails with their sender, subject, timestamp, and options to view an email or move it to the bin) -
The substance is enveloped by a <div> component with the class "table-responsive". The table is made responsive for different screen sizes using this class.
Inside the div, there is a <table> component with the classes "table" and "table-bordered". These classes are utilized to style the table.
The table header is displayed in the <thead> section with white text and a dark blue background color (#041562).
The <tr> tag addresses a table line, and the <th> labels inside it address table headers for every segment. For this situation, there are five sections: " Sender," "Subject," "Timestamp," and two buttons-free columns.
The table body, which will display each email entry, is contained in the tbody> section.
A loop that iterates over the emails variable is created by the tags "% for email in emails %" and "% endfor %." This makes the assumption that the emails variable is an iterable or list of email objects.
Inside the circle, a <tr> tag is utilized to address each email section.
The sender, subject, and timestamp of each email are displayed within each tr> with the help of td> tags, which can be accessed through the email object.
The main void section contains a <form> component that presents a POST solicitation to the "email" course when clicked. The structure incorporates a hidden information field named "emailId" that holds the worth of email.id, permitting the server to distinguish the particular email when the structure is submitted. "View Email" is the name of the button inside the form.
When clicked, the <form> element in the second empty column sends a POST request to the "/bin" route. Likewise, the structure incorporates a hidden information field named "email_id" that holds the worth of email.id. The button inside the structure is marked "Move to Bin".

layout.html - <! HTML>: DOCTYPE This statement determines that the archive is a HTML5 record.
<html lang="en">: The root element of an HTML page is the <html> element. The document's language is specified by the lang="en" attribute.
<head>: The <head> segment contains meta data about the archive, for example, character encoding, viewport settings, outside conditions, and the page title.
<meta charset="utf-8">: The document's character encoding is specified in this meta tag as UTF-8, which supports a wide range of characters.
<meta name="viewport" content="initial-scale=1, width=device-width">: This meta label sets the underlying scale and width of the viewport for cell phones.
tags like "link" and "script": These labels incorporate outside CSS and JavaScript conditions. For this situation, the code incorporates Bootstrap CSS and JavaScript records from a CDN (Content Conveyance Organization).
<interface href="/static/favicon.ico" rel="icon">: This connection label sets the favicon (site symbol) for the page. It indicates the area of the favicon record.
Link to /static/styles.css with rel="stylesheet">: A custom CSS file (styles.css) is included in this link tag for enhancing the page's styling. The file can be found in the directory /static.
Email: {%/title> block title %}{% endblock %}</title>: This sets the title of the website page. It incorporates a placeholder block {% block title %}{% endblock %} that can be superseded in youngster formats to give a particular page title.
<body>: The main content of the website can be found in the "body>" section.
<nav>: This addresses the route bar of the page. It incorporates a logo, a switch button for versatile route, and route joins. The links in the navigation change depending on whether or not the user is logged in (session["user_id"]).
Endif % and if get_flashed_messages() %: If any flashed messages (temporary notifications) are found, this code displays them in an alert box.
<main>: The page's main content can be found in this section. For a responsive layout, it has a container-fluid class and the block tag "% block main % endblock %." This block can be abrogated in youngster formats to embed explicit substance.
<footer>: The page's footer is represented by this section. A brief text contains a link to a data provider.
By and large, this HTML format sets up the construction and design of a website page. It incorporates conditions, a route bar, primary substance region, streaked messages, and a footer. Child templates can be used to extend and modify it to include specific content while keeping the same layout and structure.

login.html - <structure action="/login" method="post">: This structure component indicates the activity URL as "/login" and the technique as "post". This indicates that the data will be sent to the "/login" URL via the HTTP POST protocol when the form is submitted.
<div class="mb-3">: This div component addresses a structure field bunch with an edge base dispersing.
<input ...>: The username and password fields on the form are defined by these input elements. They have characteristics like type, placeholder, id, and name.
Log In/button>: class="button-send" type="submit" The form is submitted by means of this button element. It has a class "button-send" and shows the message "Sign In".

register.html - <structure action="/register" method="post">: This structure component determines the activity URL as "/register" and the technique as "post". It implies that when the structure is presented, the information will be shipped off the "/register" URL utilizing the HTTP POST technique.
<div class="mb-3">: This div component addresses a structure field bunch with an edge base dispersing.
<input ...>: The email, password, and confirm password fields of the form are defined by these input elements. They have characteristics like type, placeholder, id, and name.
<button class="button-send" type="submit">Register</button>: The form is submitted by means of this button element. It displays the phrase "Register" and has the class "button-send.".

reply.html - Form method="post" action="/compose">: This structure component determines the activity URL as "/form" and the strategy as "post". It implies that when the structure is presented, the information will be shipped off the "/make" URL utilizing the HTTP POST technique.
<div class="mb-3">: This div component addresses a structure field bunch with an edge base dispersing.
<label>From:</label>: The label "From:" is displayed by means of this label element.
<input ...>: A field on the form for the sender's email address is defined by this input element. It possesses id, name, style, and value attributes. The recipient's email address from the emailDetail variable is used to populate the value.
<label>To:</label>: The label "To:" is displayed by means of this label element.
<input ...>: This info component characterizes a structure field for the beneficiary's email address. It possesses id, name, style, and value attributes. The sender's email address from the emailDetail variable is used to populate the value.
<label>Subject:</label>: This mark component is utilized to show the name "Subject:".
<input ...>: An email subject form field is defined by this input element. It possesses id, name, style, and value attributes. From the variable emailDetail, the subject of the initial email is used to populate the value.
<Textarea>: For the email's body, this textarea element specifies a multi-line text input field. Name, placeholder, style, and dimension are among its attributes.
<button class="button-send" type="submit">Send</button>: The form is submitted by means of this button element. It has a class "button-send" and shows the message "Send".
It has fields for the sender, recipient, subject, and body for an email reply form. When the "Send" button is clicked, the form will be sent to the URL "/compose."

restore_confirm.html - Restore email: [h1] At the top of the page, the heading "Restore e-Mail" appears on this line.
<structure action="/reestablish affirm" method="post">: The action URL is "/restore-confirm" and the method is "post" in this form element. This indicates that the data will be sent via HTTP POST to the URL "/restore-confirm" upon submission of the form.
"emailDetail.id">: "input type="hidden" name="emailId" value="emailDetail.id" This secret info field is utilized to store the ID of the email that should be reestablished. The email's ID from the emailDetail variable is used to populate the value.
Are you sure that you want to restore this email? This passage component shows an affirmation message inquiring as to whether they are certain they need to reestablish the email.
Yes/button>: "button class="button-View" type="submit" name="confirmation" value="yes" To submit the form with a positive confirmation value, this button element is used. The word "Yes" is displayed, and its class is "button-View."
"No": "button class="button-send" "type="submit" "name="confirmation" "value="no" When submitting the form with a negative confirmation value, this button element is used. It displays the word "No" and belongs to the class "button-send."
It has a form with buttons for confirming or canceling the email restoration and hidden input for the email ID. The structure will be submitted to the "/reestablish affirm" URL when the "Yes" or "No" button is clicked.

For the CSS:
The elements that are children of the "nav" element and have the class "navbar-brand" are the focus of this selector. The text will appear to be larger when the font size is set to xx-large:
nav .navbar-brand {
    font-size: xx-large;
}

This selector focuses on the components with the class blue that are relatives of the components with the class "navbar-brand", which are thusly relatives of the "nav" component. It makes these elements appear in the dark blue color #041562:
nav .navbar-brand .blue {
    color: #041562;
}

This selector targets components with the class "list-group-item". It sets the presentation property to "flex", which empowers adaptable box design. The child elements are arranged in a row when the "flex-direction" is set to row. By setting the "justify-content" property to "space-between", the child elements are evenly distributed along the horizontal axis, with the first element at the beginning and the last at the end. The child elements are vertically aligned in the center of the container when the "align-items" property is set to center:
.list-group-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

The "view-email" class is the focus of this selector. It sets the presentation property to "flex", empowering adaptable box format. The child elements are arranged in a row with the "flex-direction" set to row. By setting the "justify-content" property to "flex-start", the child elements at the container's beginning are horizontally aligned. When the "align-items" property is set to "flex-start", the container's child elements will be vertically aligned at the container's beginning. Also, the width of the component is set to 300px:
.view-email {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    width: 300px;
}

This selector targets components with the class "center-div". It sets the presentation property to "flex", empowering adaptable box format. The "justify-content" property is set to "center", on a level plane adjusting the kid components at the focal point of the compartment. The "align-items" property is set to "center", in an upward direction adjusting the kid components at the focal point of the holder. The "flex-direction" is set to "column", organizing the kid components in a section:
.center-div {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

This selector targets components with the class "email-table". Separating the borders of adjacent table cells is accomplished by setting the border-collapse property to separate. The "border-spacing" property sets the dividing between cells to 10px:
.email-table {
    border-collapse: separate;
    border-spacing: 10px;
}

The leftover CSS code characterizes styles for different buttons. Font size, display, outline, border, cursor, background color, box shadow, padding, border radius, text color, and transitions for various states such as active and hover are among the styles. The styles of each button class—".button-send", ".button-Move", and ".button-View" are similar, but the background colors and hover effects vary.
