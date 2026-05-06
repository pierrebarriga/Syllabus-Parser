# Syllabus Parser Product 

## About the User Problem
As I finish up grad school, I noticed how much time I spent manually copying information from a PDF syllabus over to my Notion. This product aims to solve this issue. Users can upload their syllabi as a PDF and then get a CSV output with the required assignments. Read the technical details and limitations sections to make improvements.  
Please note that you will need to have an API key from Google AI Studio.

### Technical Details 
Built using Python, the code extracts text from the PDF and then feeds it into an LLM via an API. Instructions are then given to the LLM that dictates / controls the output or the repsonse. After some data wrangling / transformations the user will see the output in a tabular format and will be able to download the data directly as a CSV. 
The front end is built using streamlit. 

## Roadmap Items 
I got the idea to build this the other day and decided to spend some time to bring it to life. The user problem seemed feasible enough to build and prototype the product. If I were a Data Science PM, I would stop here to align with the engineering and design stakeholders. If I had more time to do this and build this out, I would do the following: 

### Improve Performance 
The LLM tends to take more than a minute or two in order to process all of the text. One potential solution to this would be to clean up the raw text that gets sent to the LLM. This has another added benefit in that it would reduce the amount of tokens that you are consuming. 

### Expand API Access 
Since I use Google AI Studio / Gemini during this process, I coded to just accept those LLMs. One could easily update the code, though I think further interactivity would be required to also select the appropriate model. It would be an interesting design issue to solve. 

### Upload Different Types of Files
One thing I've noticed since building -- at least in Columbia's case, professors upload their syllabus on CourseWorks directly, not allowing for a PDF output. It would be interesting if we could allow users to screenshot the assignment and then upload the screenshot. Of course, expanding to other file formats like .docx would be ideal as well. 

## Integration with Other Platforms 
We could reduce the amount of time that it takes a user to accomplish the goal of updating their project trackers by connecting directly with certain platforms. 
