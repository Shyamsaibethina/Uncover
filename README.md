#Adapt
## Inspiration

How can we use software to enforce equality? 

We asked each other what drives us in life. Feminism has been in my heart since I was a kid, but creating solutions for equality through software isn’t an obvious problem. An algorithm can’t simply get rid of centuries of deep-rooted bias. One thing I always hated was how often people would write my experiences from assault to microaggressions off as anecdotal, as it was the exception not the rule so it wasn’t a real problem. So instead of tackling equality itself, what if we could provide victims with evidence, to prove their ‘mishaps’ were a quantitative trend? Workplaces foster these microaggressions: a place people should feel welcome and comfortable. In a recent study of 2000 workers, 68% revealed they feel unsafe, or unheard in their workplace. On top of that women and other marginalized groups often feel even less important in their professional settings. We know what behaviors lead to this harsh environment: aggressive word choice, interruptions, and harsh tones. We set out to create a tool to help managers sift through countless professional conversations to make sure workers would be held accountable to create a healthier workspace. 

## What it does
Uncover analyzes workplace conversations, from direct messages, emails and even orally recorded meetings to detect microaggressions and lack of professionalism to create a safer and more welcoming environment for everyone. Managers can see employee diagnostics, through individual and team profiles with metrics such as agreeableness and coordination amongst coworkers. Uncover also provides employers with a personal note section to track how employees change their behavior over time with feedback. 

## How we built it

Like any data science project, we had to assemble our data into something comprehensive, organized, and useful. To target speech, we used Google Cloud’s speech to text API to transcribe conversations, detect speakers, and generate time stamps. We can then assemble this into a corpus - a high level semantic data structure that represents speakers, utterances of speech, and the text itself in the context of each other. We used Convokit to get metrics to represent a person’s speech patterns, and their agreeableness in the context of other people. Using the data Convokit analyzed from the speech, we designed a function to summarize and represent the data from the workplace more clearly so that managers can read through the data easily. To present this data aesthetically, we used Streamlit to provide a user-friendly experience for managers to accurately assess their workplace, identify weaknesses, and create a course of action. 

The google cloud API call:

![Google Cloud Speech-to-Text API usage in our project](https://github.com/Shyamsaibethina/Uncover/blob/main/assets/google-cloud.png?raw=true)

## Challenges we ran into
Defining a person’s profile through numbers can be limiting. Deciding how to display numbers in a comprehensive and understandable way to users was challenging. We decided to rank the scores of the employees on the profile, because identifying weak points is an important pathway to growth. Utilizing the Google Cloud Speech to Text API proved very difficult as most implementations for speech diarizations are not currently functional. We solved this by creating clearer data that helped the model learn more about our voices before making judgment calls. Additionally, Streamlit sacrifices customization for speed, so we had to utilize Markdown and HTML in order to change the margins, fonts, and sizes of elements to create a more aesthetically pleasing application.

## Accomplishments that we're proud of
Convokit was created to analyze text, through harnessing Google Cloud APIs we figured out a way to analyze speech, giving employers more leeway on the types of acceptable input data. Synthesizing multiple pieces of software and defining our own algorithms allowed us to build upon other’s work to create products that more people can use and find applicable. The thing that we are most proud of though is creating solutions to a problem that does not have a clear answer yet affects so many people. We can introduce logic and code to make the world a little more fair. 

## What we learned
We learned how to use Google Cloud APIs, Convokit, and Streamlit. More important than learning these powerful technologies, we learned the art of reading documentation - how to take existing projects and make them functional for our usage. NLP was an essential skill we developed through this project as our idea demands human-like analysis of speech and text. Our data science skills and data manipulation improved over the course of working. Beyond extra technical skills, creating a working prototype of a project in a few hours can prove to be tiring and difficult for a number of reasons. We learned to each play to our strengths rather than control every aspect of the presentation. We regularly continued to talk about our progress to update each other and clarify we all had the same end goal in mind to create one project, not parts of a project that are related. We learned how to create detailed and organized plans to attack problems rather than aim in the dark for results.

## What's next for Uncover
Ideally the whole process from getting data to displaying results would be automated. Uncover would be able to take in data from company emails, webex, slack and recorded meeting calls to create more accurate analysis of a team. Eventually it would be able to detect inflections in voice to account for sarcasm, humor and more edge cases. A world where managers can use this tool to accurately understand workplace dynamics is one that’s safer, brighter, and thanks to the art of CS a little bit easier. 

Our team:
![Our team!](https://github.com/Shyamsaibethina/Uncover/blob/main/assets/team.jpg?raw=true)
