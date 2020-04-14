# Damien Meere - BT Ireland
### Practical Python and Data-Centric Development Milestone Project- Code Institute

This project website will highlight my capability to employ the various tools illustrated throughout the Practical Python and Data-Centric Development section of the Code Institute 
programme. 

This project will present a training course booking site, which facilitates the trainer in Creating, Viewing, Editing and Deleting training courses. On creation of a new course,
the trainer specifies the maximum number of subscribers a course can take. In defining this value, only that number of trainees will be permitted to enroll on the course. All elements
of the courses are editable except for the maximum subscriber value. On the trainer view, the trainer can quickly view what the uptake levels are for each course with a progress bar.
The site also enables trainees to view course informaiton, and view the uptake level. And once they have chosen a course, upon submission of their name and email, they will be given 
feedback as to whether their request has been successful of if there are no remaining spaces on a course.

No User Authentication was incorporated into this project, as this is considered beyond the scope of this section of the course. Rather there will be an anonymous Trainer and trainee
area within the site.

## Table of Contents

- [Demo](#Demo)
- [Database](#Database)
- [UX + User Stories](#UX+User-Stories)
- [Technologies](#Technologies)
- [Site Notes](#Site-Notes)
- [Current Features](#Current-Features)
- [Future Features](#Future-Features)
- [Testing](#Testing)
- [Testing -  Unresolved Bugs](#Testing-Unresolved_Bugs)
- [Deployment](#Deployment)
- [Internal Deployment](#Internal-Deployment)
- [Acknowledgements](#Acknowledgements)
- [Content](#Content)

## Demo
A live demo of the project can be found deployed to Heroku [Here](https://dm-milestone-3-code-institute.herokuapp.com/)

## Database
![Database Structure](documentation/database_v2.jpg)

The database itself is stored on [MongoDB](https://www.mongodb.com/). the structure consists for 4 collections. The category, course_duration and course_size collections are utilised
to faciliate more a strucutred approach to course creation. On the course creation pag, these three collections faciliate dropdown menus on the page. The elements of each of these
collections can be created, viewed, edited and deleted from the 'Manage Course Utilities' menu in the site navbar.

The course collection houses the main objects of the site. information relating to all aspects of the course are stored here. This collection is queried to populate the 'accordian'
elements on the main page of the trainer and trainee sections. The percentage value houses an updated string value identifying the current uptake level on the course. As trainees enroll
in courses, this value is updated. The Subscriber_list contains a nested collection of key/value pairs identifying the name and email of all trainees that have requested access 
to a course.


## UX+User-Stories
![Responsive Views of Home Page](documentation/responsive_view.jpg)

My goal in building this site was to make it easier to observe and manage information related to training activites within BT Ireland through a simple, easily navigated interface. 
In this process there are two types of actors - Trainers & Trainees. Therefore, in designing this site, I started with the following user stories:

***Trainer Building and diseminating information related to training programmes
> I wanted easy trainers to be able to create, access, edit and delete information on available training options through a minimalist, sleek, easy-to-navigate site. I wanted the 
trainer to be able to create a course, but to still be directed in some aspects of the course creation. Therefore, a number of fields of the course creation and course editing pages
are populated dropdown menus (Category, Duration & Size), where the contents of the dropdown come from the requisite collections in the [database](#Database). Of course these elements
are not static, and as such, each collection can be all be managed (created, viewed, edited, deleted) from the Manage Course Utilities menu. I also wanted the trainer to be able to 
quickly ascertain the uptake on each course to view the amount of enrollments for each course, so I chose to represent this as a progress bar that gives a quick visual breakdown 
of the enrollments. 

***Trainee Looking to access course information and enroll in their chosen programme
> I wanted to faciliate a view of the information for trainees where they could get all the information they might require about a particular course and enroll in their chosen 
courses. On submission of an enrollment, should there be sufficient space to accomodate the trainee, they are presented with feedback to confirm their space. If ther is not space 
available, the feedback is presented to notifiy the trainee.

From these user stories, it was clear that quick and easy access to information would be key to ensuring that users could make the most efficient use of the Trainer and Trainee 
interfaces. I needed to make sure that users could quickly navigate the site, and locate any course information they required with minimal prompting. As illustrated by the images 
in the [Wireframes folder](wireframes), even from the early designs, I wanted to ensure thesite was easy-to-navigate and use. As youc an see from the completed 
[project site](https://dm-milestone-3-code-institute.herokuapp.com/), the final version has not strayed far from the originally intended designs.

One alteration is that both trainer and trainee interfaces are easily acessible from the navbar. There is no site authentication in this project, so for demonstrative purposes, 
visitors can quickly move back and forth between the interfaces. In order to ensure continued usability, regardless of accessing device, responsive design has been incorporated to
the project. 


## Technologies
This project utilises the following technologies:
1. [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
2. [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
3. [Javascript](https://www.w3schools.com/jsref/)
4. [Python](https://www.python.org/)
5. [MongoDB](https://www.mongodb.com/)
6. [Materialize](http://archives.materializecss.com/0.100.2/) (0.100.2)
7. [FontAwesome](https://fontawesome.com/)
8. [JQuery](https://jquery.com)
9. [Git](https://git-scm.com/)
10. [Flask](https://flask.palletsprojects.com/en/1.1.x/)


## Site-Notes
As detailed in the [UX + User Stories](#UX+User-Stories) both trainer and trainee interfaces are accessible from the navbar. There is no site authentication in this project, so for 
demonstrative purposes, visitors can quickly move back and forth between the interfaces. 

## Current-Features

Provide Page breakdowns here



## Future-Features
Authentication, Authorisation and Accounting: In the next iteration of this project (see [Internal Deployment](#Internal-Deployment)) user Authentication will be required, utilising internal BT infrastructure.

A [Training Dashboard](https://damien-meere.github.io/interactive_frontend_milestone/) was developed in a previous milestone project. The next step in the evolution of this tool will be to interconnect the two tools, and utilise the dashboard to interogate the dateset generate through the continued use of this tool by both Trainers and Trainees within BT. 

Another useful feature will be to faciliate ongoing easy to understand feedback for both the Trainers and Trainees. Each course will be able to determine the popularity/success of a progamme by enable using to gia ve course an Upvote or a Downvote.This feedback will enable trainees to quickly ascertain how other trainees have felt about a programme before proceeding to enroll.

Finally, on successful enrollment in a programme, a useful feature will be to automatically email the trainee with the requisite joining instructions whether the course is online 
(link to requisite platform) or classroom-based (location and access requirments).

## Testing

Form verifiction testing - with valid data,  without any data, with partial data - Compulsory fields

Validation of User stories

Responsive Design


All CSS, HTML and Javascript files were passed through code validators. The [CSS Validator](https://jigsaw.w3.org/css-validator/) & [HTML Validator](https://validator.w3.org)
checked the markup validity of Web documents against the w3c standards. the [JSHint](https://jshint.com/) utility was used to check for errors and potential problems in the
JavaScript code.

All links on each page were individually tested to ensure they navigated to the requisite page.

This site was tested across multiple browsers (Chrome, Safari, Firefox), and on multiple devices (Samsung Galaxy S8/S9/S10, Samsung Galaxy Tab, Apple iPad, iPhone 6/7/8)
to ensure compatibility and responsiveness. As detailed in the next section, the display of charts is somewhat unresponsive on smaller screens, and the current iteration
is suited to desktop presentation.

## Testing-Unresolved_Bugs

On the course creation page, all the fields are set as required forcing the user to complete all fields befor ethe form can be submitted. Unfortunately, Because each input is readOnly 
by default, HTML5 attributes, such as required, do not get enforced. Therefore the user can submit the course creation form without specifying the date.


## Deployment
A live iteration of this project can be found deployed to [Heroku](https://dm-milestone-3-code-institute.herokuapp.com/)

To run locally, you can clone this repository directly into the editor of your choice by pasting `git clone https://github.com/damien-meere/Data-Centric-Development-Milestone-Project.git` 
into your terminal. To cut ties with this GitHub repository, type `git remote rm origin` into the terminal.

You can also Clone this Repository to GitHub Desktop, by navigating to the [main page](https://github.com/damien-meere/Data-Centric-Development-Milestone-Project) of the 
repository on GitHub, under the repository name, click Clone or download. Click Open in Desktop to clone the repository and open it in GitHub Desktop. Click Choose... and, 
using Windows Explorer, navigate to a local path where you want to clone the repository. For more information you can 
review the [GitHub site](https://help.github.com/en/articles/cloning-a-repository#cloning-a-repository-to-github-desktop).

## Internal-Deployment
Use within BT - This is a test portal which I aim to use to faciliate booking to courses and training sessions within BT. This protal will be deployed internally within the 
company's Intranet, with the code being housed within internal infrastructure. Using this portal, training managers will be able to circulate information relating to upcoming 
courses, and faciliate more effective and efficient administration of these training programmes. As detailed in the [Future Features](#Future-Features) section, the next iteration 
will require integration within internal BT AAA infrastructure to ensure adequate security.

### Acknowledgements



### Content
All data contained within this site is mocked up.

**This site is for educational purposes**
