# FootyGraphs

## Overview

This Python program analyzes and visualizes key statistics from teams in the Bundesliga and Premier League. It combines the power of data analytics with user-friendly visualization, leveraging **Matplotlib** for plotting and **Tkinter** for an interactive graphical interface. The application provides insightful comparisons and trends, offering a comprehensive look at the performance of teams in these top football leagues.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Example Usage](#example-usage)
4. [Lessons Learned](#lessons-learned)
5. [Future Enhancements](#future-enhancements)

## Features

- **Real-Time Data Scraping**: Automatically fetches up-to-date statistics from **Fbref.com** for the selected league.
- **Interactive Graphical Interface**: A user-friendly **Tkinter** application that facilitates exploration.
- **Dynamic Visualizations**: Choose from four distinct **Matplotlib** plots to analyze team statistics and trends.

## Technologies Used

- **Python**: Core programming language.
- **Matplotlib**: For creating data visualizations.
- **Tkinter**: For building the graphical user interface.
- **Pandas**: Scrapes the data from Fbref.com, manipulates data to create data visualizations. 
- **Numpy**: Used to create test method

## Example Usage

When the program is executed, it scrapes data from Fbref.com about the chosen league. The example usage is done with the Bundesliga chosen but the program is functional with the Premier League. The user is then presented with four different buttons, each of which displaying a different matplotlib plot within the tkinter applcation:

### Initial Start
With randomized data. See [Future Enhancements](#future-enhancements):

![Screenshot 2024-12-22 195253](https://github.com/user-attachments/assets/df44ac7c-b2a4-4861-abcd-1de3ed524aa1)

### Expected Goals Vs. Actual Goals

![Screenshot 2024-12-22 203657](https://github.com/user-attachments/assets/a9a56469-4120-4975-8fe5-a3bb3bd13907)

### Expected Goals Against Vs. Actual Goals Against

![Screenshot 2024-12-22 203705](https://github.com/user-attachments/assets/6308202a-d372-4d1e-bae3-ba498edcb0bf)

### View Attendance

![Screenshot 2024-12-22 203712](https://github.com/user-attachments/assets/80207c9c-063b-45d0-86ee-07a679755bb5)

### Goals Pie Chart

![Screenshot 2024-12-22 204017](https://github.com/user-attachments/assets/7714dacb-4511-4e10-a2c6-deee0ad519b7)


## Lessons Learned

- **Matplotlib**: Gained experience in creating various types of data visualizations, including bar charts, heatmaps, pie charts, and scatter plots, and learned how to customize plots for clarity and aesthetics.  
- **Pandas**: Improved skills in handling and analyzing datasets, including filtering, cleaning, and summarizing data to extract meaningful insights.  
- **Web Scraping with Pandas**: Learned how to combine **BeautifulSoup** and **Pandas** to scrape data from web pages and directly load it into structured dataframes for analysis.  
- **Tkinter**: Developed expertise in building user-friendly graphical interfaces, including buttons and interactive elements, to integrate visualizations into a standalone application.  

## Future Enhancements

Reflecting on this project, I see several ways to enhance and expand its capabilities:

- **Get Around Fbref.com scraping protection**: When beginning this project, Fbref.com was cooperating, and allowed scraping of their table. Recently, they have reduced permissions in scraping their site. (Which is why the pictures in this README are with randomly generated data). In the future, I plan on experimenting on ways to get around this, and create a functional program again. 
- **Add Increased Functionality**: I plan on adding a bar that can easily swap between leagues. There is currently functionality for Bundesliga and the Premier league, but I want functionality for the top five European Leagues.
-  **Add Serie A, Ligue 1, La Liga, and Champions League Functionality**: This is a simple addition that I haven't gotten around to yet, adding functionality for each league. 
