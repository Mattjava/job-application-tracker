# Tools Used

- Claude AI

# Prompts

- Hey, can you please set up the HTML templates? The 4 out of the 6 tables refer to showing data in the tables. Users are allowed to add, edit, and delete data into the tables. The sole exceptions are job_match.html and dashboard.html. Dashboard should show the users the amount of jobs they applied to, interviewing at, and other useful statistics. Job match should show what's being rendered in more fleshed out format.  Do not touch the backend, but you can read it for reference. Also avoid writing CSS for now. Create other HTML files if needed.

- It is now time to work on the CSS. I am using Bootstrap for this project; I have already set it up in the backend (app.py). Your goal is to apply it to apply it to the HTML. I was thinking of going for a minit (green - white) color palette for the website. Be sure you pay close attention to the spacing of the tables.

# What Worked

- Supplied a basic HTML template to work with
- Created a smooth UI with CSS and Bootstrap

# What You Changed

- References to backend functions and routes were changed to use url_for. This makes it easier to better understand the code
- Supplied values from the backend into the UI. Claude didn't set up the inputs for rendering, so I have to put in the work
- Changed some references to a function. For example, I changed a function's name, so I have to step into the HTML and change it there as well. 

# Lessons Learned