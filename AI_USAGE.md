# Tools Used

- Claude AI

# Prompts

- Hey, can you please set up the HTML templates? The 4 out of the 6 tables refer to showing data in the tables. Users are allowed to add, edit, and delete data into the tables. The sole exceptions are job_match.html and dashboard.html. Dashboard should show the users the amount of jobs they applied to, interviewing at, and other useful statistics. Job match should show what's being rendered in more fleshed out format.  Do not touch the backend, but you can read it for reference. Also avoid writing CSS for now. Create other HTML files if needed.

- It is now time to work on the CSS. I am using Bootstrap for this project; I have already set it up in the backend (app.py). Your goal is to apply it to apply it to the HTML. I was thinking of going for a minit (green - white) color palette for the website. Be sure you pay close attention to the spacing of the tables.

- Hey Claude. I am adding a new column into the application table: Interview data. InterviewData is a JSON column that contains the number of interview rounds (interview_rounds), an array of interviewer names (interviewers), an array of technical questions (technical_questions), an array of feedback regarding the interview (feedback), the next steps as a string if the application is not finished (next_steps), and a rating for a completed application process (rating).

Additionally, requirements column on the jobs table is now expanded to have required skills (required_skills), preferred skills (preferred_skills), the education needed (education), experience needed (experience_years), and whether or not it is a remote job (remote_option).

# What Worked

- Supplied a basic HTML template to work with
- Created a smooth UI with CSS and Bootstrap
- Help expand the input of tables in response to a new column being added to the tables
- Supplied and suggested backend bug fixes that helped me create a better server

# What You Changed

- References to backend functions and routes were changed to use url_for. This makes it easier to better understand the code
- Supplied values from the backend into the UI. Claude didn't set up the inputs for rendering, so I have to put in the work
- Changed some references to a function. For example, I changed a function's name, so I have to step into the HTML and change it there as well. 
- Changed various aspects of the UI. For example, I re-organized the statues list on the dashboard. I felt the original design made by the AI did not meet the needs of the user, so I went ahead and re-arranged them by hand.
- Added some decorations to the AI generated code. For example, the icon in the top left corner was not added in by AI. I added it in since it looks more nicer there than what AI had originally.

# Lessons Learned

- AI is a useful tool for creating long pieces of code while letting you focus on other tasks. However, it is not perfect.
- AI is prone to making mistakes, so you are still responsible for looking over and fixing what it misses.
- AI also does not truly understand the design on your project. It is limited to what you feed it, so it can't see important aspects of the app such as user's needs
- AI can be a crutch at times, letting you generate code and funtions you do not know. However, you are still expected to know how it works. Additionally, if something breaks, having prior knowledge is useful in fixing them.