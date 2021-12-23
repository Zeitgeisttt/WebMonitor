# WebsiteMonitor

Inspired and based on the work of [Zack Scholl](https://github.com/schollz) and his [blog](https://schollz.com/blog/pottery).  
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

Actually, you can customize  
1. The website you want to monitor  
2. The automatic email sender 
3. The threshold of structural similarity you need
4. The time interval that you check the webpage for changes

#### 1. website
In any of the .sh files, you can change the link after "--url" to any website you want to monitor for changes.
#### 2. email sender
The emails are sent automatically using SMTP servers. The default email sender ("newhouseavailable@163.com") was created by me using the SMTP server of 163.com, but you can create your own account! (Google how.) Once you do, you need to update (in the .sh file) the email address after "--smtpemail" along with the password after "--smtppass" to your account's address and password. Also, if you use a different SMTP server from 163.com, you need to change Line 64 of "webmonitor.py":
```
s = smtplib.SMTP_SSL("smtp.163.com", "465")
```
Change "smtp.163.com" and "465" to your SMTP server and port respectively.
#### 3. threshold
Sometimes you may not want to be notified of every small change on the webpage, but only the big ones. So you can change the value after "--threshold" in the .sh file. The threshold controls how small the structural similarity (how big the change on website) needs to be for us to get notified. The structural similarity between the two recent screenshots checks the extent of website changes, with 1.0 being the website stays the same and the smaller the value (between 0 and 1) is, the greater the change is. The default is set to be 0.95 so that the change that new houses have been put on the website can be captured. 
#### 4. time interval
You can change the value after "--sleep" in the .sh file to control how often we check the website for changes. The default is 30, which means we check the website every 30 seconds so that you will get notified in at most 30 seconds after the website changes. This is a tradeoff between how quickly you get notified and how much CPU/Memory you want this program to use.

## References
Thanks again to the inspiration of Zack Scholl's [blog](https://schollz.com/blog/pottery)!  
Other References:  
&ensp;[skimage.metrics.structural_similarity](https://scikit-image.org/docs/dev/api/skimage.metrics.html#skimage.metrics.structural_similarity)  
&ensp;[Carlos Delgado's article on SSIM](https://ourcodeworld.com/articles/read/991/how-to-calculate-the-structural-similarity-index-ssim-between-two-images-with-python)  
&ensp;[click](https://click.palletsprojects.com/en/8.0.x/)  
&ensp;[loguru](https://loguru.readthedocs.io/en/stable/)  
&ensp;[puppeteer](https://github.com/puppeteer/puppeteer)

## License
MIT
