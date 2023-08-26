# TedUp

[![> Research Paper](https://img.shields.io/badge/Research%20Paper-blue)](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/blob/main/Virtual%20Therapist.pdf)
[![> Notebook & dataset](https://img.shields.io/badge/Notebook%20Dataset-red)](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/tree/main/Deep%20Learning%20training/model_v1.1)
[![> Video Demo](https://img.shields.io/badge/Video%20Demo-yellow)](https://www.youtube.com/watch?v=4ihejsiQ43E&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&pp=iAQB)
[![> Pitching slide](https://img.shields.io/badge/Pitching%20slide-black)](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/blob/main/LHP%20Team%20-%20Virtual%20Therapst.pdf)
[![> All models](https://img.shields.io/badge/All%20models-white)](https://drive.google.com/drive/folders/16ig9NcXq4Cn39F2h7c8YvgRFNaegVj7F?usp=sharing)




## New UI and new updated functions
- Released version of Vietnamese for the chatbot and progess recorder
- New clean minimal UI
- New podcast playlists
- Blogs query by tags
- Hybrid recommender system

[LINK VIDEO DEMO HERE]()





## Abstract & introduction

Adolescents are facing various challenges to their mental health due to their exposure to online risks and pressures, such as cyberbullying, misinformation, social comparison, and unrealistic expectations. They also have to deal with the stress and anxiety from their academic and personal lives, which can affect their self- esteem and well-being. These factors can lead to negative emotions and behaviors, such as depression, isolation, self-harm, and substance abuse. Teenagers are reluctant to ask for help because of the stigma around mental health disorders, and there are also additional limitations including waiting lists and geographic restrictions. There is a significant gap in the treatment that should be available conveniently and cost-effectively, and the services available at hand. The ratio of therapists, psychiatrists, psychiatric social workers and mental health nurses to patients is 1: 10,000, even in developed countries (Kislay, 2020). The disparity in the system means that most people with menta health problems will never get the support the need. In response, we developed a technology-based application that provides online support and guidance to adolescents with mental health
problems.

## Approach

The application uses natural language processing and artificial intelligence to interact with users in a conversational manner, and offers a toolbox of features to help them cope with stress, anxiety, depression, and other challenges. The application also integrates mental health assessment tools to monitor the users’ progress and provide

feedback. We assume that technology-based applications can be a viable and scalable alternative to face-to-face mental health services for adolescents. Our solution consists of four main components:

- A general emotion classifier that can categorize the user’s story (diary) into positive, negative, or neutral emotions, based on a deep neural network with bidirectional LSTM (BiLSTM) architecture. We evaluated our solution using a self-scraping dataset of online diaries from various websites. We compared different architectures and models for each component and selected the best ones based on their accuracy and performance.
- A complex emotion classifier that can further classify the user’s story into 12 fine-grained emotion categories, such as anger, sadness, remorse, fear, depression, lonely, joy, love, optimism, gratitude, and pride. This component uses a transfer learning approach with BERT pretrained model to achieve better performance. The results from this step are then used to quantify the user’s mental health quality based on a our mathematical formula.
- A chatbot that can respond to the user’s story with empathetic and supportive messages, and suggest some practical solutions to help them cope with their negative emotions and improve their well-being.
- We have a time series analysis model that can predict the user’s future emotional trends based on their past diary entries. This component can help the user monitor their progress and identify potential risks or opportunities for intervention. (This feature need time to be improved)
- Finally, there is a recommender system using neighbourhood collaborative filtering to suggest the best=fit blogs that can solve problems for users in a personalized way.


## Explore the product's features
### Q-system (Emotions Classifications and Q-value function)
[View now](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/tree/main/src)

### Recommender System (User-to-user collaborative filtering)
[View now](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/blob/main/templates/README.md)

## Playlist Video Demo
[Link to playlist](https://www.youtube.com/playlist?list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV)

- [Overall walkthrough of our product](https://www.youtube.com/watch?v=4ihejsiQ43E&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&index=1)
- [Chatting and monitoring your mental health progress](https://www.youtube.com/watch?v=O9DBS1uLPKc&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&index=2)
- [How to signup, login, and create post](https://www.youtube.com/watch?v=ylvl6Ik4gDw&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&index=3)
- [Recommender System](https://www.youtube.com/watch?v=iaAHY0NucaI&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&index=4)
- [Q-system (Emotions classifications and Q-value functions)](https://www.youtube.com/watch?v=NkX4Q-JG3D4&list=PL49eoaM3kiojx1y0D4b31UdhEM9SMfriV&index=5)

# What's next
- Expand the dataset to make the AI model more generalized and practical
- Impove the time series for progess record analyis 
- Solve the "cold start" problem of the recommender system

## How to run the code
First you need to clone this repository to your local system. Open terminal and then paste this command line
```
git clone https://github.com/Hackathon-LHP-Team/Virtual-Therapist.git
```
Next move into the cloned directory
```
cd Virtual-Therapist
```
(optional) Type this to open your default code editor. As usual, it will open vscode if you use vscode as your default code editor
```
. code
```
Create a virtual environment with venv to avoid conflicts in library versions and modules
```
python -m venv .venv
```
Activate the environment
```
.\.venv\Scripts\activate
```
Install all neccessary libraries with a specific version
```
pip install -r requirements.txt
```
Now if you want to view all libraries and modules in your virtual environment, paste this command line
```
pip freeze
```
To run the server backend flask python, run this line of command
```
flask --debug run
```
Now, the website should be available at the port `127.0.0.1:5000`

To run the streamlit app, move into the `src` folder
```
cd src
```
Now run the app with this command
```
streamlit run main.py
```

## Code Structure
        ├───src
    │   ├───assets
    │   └───.streamlit
    ├───templates
    ├───.git
    │   ├───hooks
    │   ├───objects
    │   │   ├───pack
    │   │   └───info
    │   ├───info
    │   ├───refs
    │   │   ├───tags
    │   │   ├───remotes
    │   │   │   └───origin
    │   │   └───heads
    │   └───logs
    │       └───refs
    │           ├───remotes
    │           │   └───origin
    │           └───heads
    ├───instance
    ├───Deep Learning training
    │   └───model_v1.1
    │       ├───dataset
    │       ├───imgs
    │       └───models
    ├───Research Papers
    ├───static
    │   ├───imgs
    │   ├───scss
    │   ├───css
    │   ├───js
    │   └───vendor
    │       ├───purecounter
    │       ├───bootstrap
    │       │   ├───css
    │       │   └───js
    │       ├───swiper
    │       ├───glightbox
    │       │   ├───css
    │       │   └───js
    │       ├───bootstrap-icons
    │       │   └───fonts
    │       └───typed.js
    └───migrations
        └───versions
