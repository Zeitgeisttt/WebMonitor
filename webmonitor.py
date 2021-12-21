import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import urllib.request

# install packages with
# python3 -m pip install click numpy loguru scikit-image opencv-python

import click
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from loguru import logger

# use hosts file to remove ads
hostsfile = "http://sbc.io/hosts/alternates/fakenews-gambling-porn-social/hosts"

# The key idea is to regularly compare the old and new screenshots of a website to monitor any changes
# If there are, send an email to specified address using SMTP

def compare_images(img1, img2):
    # load two images in grayscale mode
    old_gray = cv2.imread(img1, 0)
    new_gray = cv2.imread(img2, 0)

    # write a copy of the new image with specified filename
    new = cv2.imread(img2)
    cv2.imwrite("new.jpg", new, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    # compute the SSIM (structural similarity index) between the two grayscale images
    # float mssim (mean SSIM) represents the similarity between images (1.0 for identical images)
    # mssim will be compared to a threshold
    #   so that we only get notified when the website changes significantly
    try:
        (mssim, diff) = ssim(old_gray, new_gray, full=True)
    except ValueError as err:
        if str(err) == "Input images must have the same dimensions.":
            # images have different dimensions
            # which means the website changed!
            return 0
        else:
            raise err

    return mssim

# send email using functions from email.mime
def send_email(smtpemail, smtppass, to, subject, messagebody, imgname):
    img_data = open(imgname, "rb").read()
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = smtpemail
    msg["To"] = to

    text = MIMEText(messagebody)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(imgname))
    msg.attach(image)

    # this can be changed to any other smtp email services.
    s = smtplib.SMTP_SSL("smtp.163.com", "465")
    s.ehlo()
    s.login(smtpemail, smtppass)
    s.sendmail(msg["From"], msg["To"], msg.as_string())
    s.quit()

@click.command()
@click.option("--folder", default=".", help="directory to store data")
@click.option("--url", help="url to watch", required=True)
@click.option("--css", default="full", help="CSS selector of element to watch, default full page")
@click.option("--to", help="email address of person to alert")
@click.option("--smtpemail", default="", help="SMTP email address")
@click.option("--smtppass", default="", help="SMTP email password")
@click.option("--threshold", default=1.0, help="threshold for sending email")

def run(folder, url, css, to, smtpemail, smtppass, threshold):
    logger.debug("changing dir to {}", folder)
    os.chdir(folder)
    with open("index.js", "w") as f:
        f.write(indexjs)

    # we use puppeteer to generate screenshots of webpages
    if not os.path.exists(os.path.join("node_modules", "puppeteer")):
        logger.debug("installing puppeteer in {}", os.path.abspath("."))
        os.system("npm i puppeteer")
    if not os.path.exists(os.path.join("hosts")):
        logger.debug("downloading hosts file {}", hostsfile)
        urllib.request.urlretrieve(hostsfile, "hosts")
    node_cmd = "node index.js " + url + " new.png '" + css + "'"
    logger.debug(node_cmd)
    os.system(node_cmd)
    if os.path.exists("last.png"):
        logger.debug("comparing images")
        similarity = compare_images("last.png", "new.png")
        logger.debug("similarity: {}", similarity)
        if similarity < threshold and smtpemail != "" and smtppass != "" and to != "":
            logger.debug("similarity < 0.99, sending email")
            logger.debug(os.path.join(os.path.abspath("."), "new.jpg"))
            send_email(
                smtpemail,
                smtppass,
                to,
                "web change " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                url,
                os.path.join(os.path.abspath("."), "new.jpg"),
            )
        os.remove("last.png")
    logger.debug("saving new image")
    os.rename("new.png", "last.png")

indexjs = r"""
const fs = require('fs');

const puppeteer = require('puppeteer');

hosts = {};
//now we read the host file
var hostFile = fs.readFileSync('hosts', 'utf8').split('\n');
var hosts = {};
for (var i = 0; i < hostFile.length; i++) {
    if (hostFile[i].charAt(0) == "#") {
        continue
    }
    var frags = hostFile[i].split(' ');
    if (frags.length > 1 && frags[0] === '0.0.0.0') {
        hosts[frags[1].trim()] = true;
    }
}

(async () => {

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.setRequestInterception(true)

    page.on('request', request => {

        var domain = null;
        var frags = request.url().split('/');
        if (frags.length > 2) {
            domain = frags[2];
        }

        // just abort if found
        if (hosts[domain] === true) {
            request.abort();
        } else {
            request.continue();
        }
    });
    // Adjustments particular to this page to ensure we hit desktop breakpoint.
    page.setViewport({ width: 1000, height: 1000, deviceScaleFactor: 1 });

    await page.goto(process.argv[2], { waitUntil: 'networkidle2' });
    await page.waitFor(5000);

    if (process.argv[4] == 'full') {
        await page.screenshot({
            path: process.argv[3],
            fullPage: true
        })
        await browser.close();
        return
    }
    /**
     * Takes a screenshot of a DOM element on the page, with optional padding.
     *
     * @param {!{path:string, selector:string, padding:(number|undefined)}=} opts
     * @return {!Promise<!Buffer>}
     */
    async function screenshotDOMElement(opts = {}) {
        const padding = 'padding' in opts ? opts.padding : 0;
        const path = 'path' in opts ? opts.path : null;
        const selector = opts.selector;

        if (!selector)
            throw Error('Please provide a selector.');

        const rect = await page.evaluate(selector => {
            const element = document.querySelector(selector);
            if (!element)
                return null;
            const { x, y, width, height } = element.getBoundingClientRect();
            return { left: x, top: y, width, height, id: element.id };
        }, selector);

        if (!rect)
            throw Error(`Could not find element that matches selector: ${selector}.`);

        return await page.screenshot({
            path,
            clip: {
                x: rect.left - padding,
                y: rect.top - padding,
                width: rect.width + padding * 2,
                height: rect.height + padding * 2
            }
        });
    }

    await screenshotDOMElement({
        path: process.argv[3],
        selector: process.argv[4],
        padding: 16
    });

    browser.close();
})();
"""


if __name__ == "__main__":
    run()
