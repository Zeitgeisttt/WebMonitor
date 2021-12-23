# WebsiteMonitor

Inspired and based on the work of Zack Scholl and his [blog](https://schollz.com/blog/pottery).  
A version of Website Change Monitor he created using Go and Node.js can be found [here](https://github.com/schollz/websitechanges).  

This project aimed to help UCSD international students (including myself) find houses by monitoring the websites of leasing offices near campus for newly available houses.  

When I was in China during the pandemic, the only way to rent houses for the Fall 2021 quarter was through leasing offices’ websites. However, demand exceeded supply. 
So I created a program that could monitor the leasing offices’ websites for newly available houses. 
The program will send you an email notification when new houses become available on leasing offices' websites, along with a screenshot of the webpage.  

## Example

When the website changes (which means new houses are available), the specified email address will receive an email notification along with the link and the screenshot of the website. Here's what we would receive when new houses become available on the webpage of Towers's leasing office while we are running Towers.sh in the Towers/ directory.

<pre align="center">Email Example              Attachment Example
<p align="center">
<img src="https://user-images.githubusercontent.com/42275000/147168575-124933d9-6120-4235-867e-3fceaf93214c.jpg" width="200" height="400">  <img src="https://user-images.githubusercontent.com/42275000/147168572-5649f959-3bb0-409b-9879-27b8065e71d2.jpg" width="200" height="400">
</p>
</pre>

## Usage

First, install required packages using pip:
```
pip install click numpy loguru scikit-image opencv-python
```
Then, change the "example@xxx.com" in the .sh file to your email address.  

You can now run the .sh file in the command line by entering ./xxx.sh under its directory!

## Customization

You 
