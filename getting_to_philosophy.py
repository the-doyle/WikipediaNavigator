from bs4 import BeautifulSoup
import requests 
import sys

class PhilosophyNavigator:
    def __init__(self, startURL):
        self.rootURL = "https://en.wikipedia.org" 
        self.target = "/wiki/Philosophy" #could be swapped out to test other targets 
        self.startURL = startURL.split("org")[1] 
        self.prevURL = startURL.split("org")[1]
        self.destinationURL = "" 
        self.path = [] 
        self.hops = 0

    #helper function to determine if an href is valid 
    def hrefIsValid(self, href):
        if href \
            and "/wiki/" in href \
                and "(" not in href \
                    and href != self.startURL:
                        return True 
        return False 

    #helper function to find first valid link on page, or return None if page contains no valid links
    def getFirstLink(self, slug):
        res = requests.get(self.rootURL + slug)
        html = res.text 
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        
        for p in paragraphs:
            links = p.find_all('a')
            if links:
                for link in links:
                    href = link.get('href')
                    if self.hrefIsValid(href):
                        return href  

        return None  

    #helper function to print output 
    def printOutput(self, result):
        if result == "success":
            for link in self.path:
                print(link)
            print(f"{self.hops} hops")

        elif result == "circular":
            print(f"A circular path has been detected between {self.startURL} and {self.destinationURL}")
            print(f"This path was located after {self.hops} hops")

        elif result == "maxHops":
            print(f"100 hops reached. The most recently visited page was {self.prevURL}")

        else:
            print(f"The most recently visited page {self.startURL} did not contain any links")

    #main function 
    def findPhilosophy(self):
        while self.hops < 100:
            #if we have successfully navigated to Philosophy page
            if self.startURL == self.target:
                self.path.append(self.rootURL + self.startURL)
                self.printOutput("success")
                return  

            #get first link on page 
            self.destinationURL = self.getFirstLink(self.startURL)

            #page has no links
            if not self.destinationURL:
                self.printOutput("noLinks")

            #first link on page links back to previous page 
            if self.destinationURL == self.prevURL:
                self.printOutput("circular")
                return 
            
            #first link is valid, continue 
            else:
                self.path.append(self.rootURL + self.startURL)
                self.hops += 1 
                self.prevURL = self.startURL 
                self.startURL = self.destinationURL

        #if hops == 100
        self.printOutput("maxHops")

p = PhilosophyNavigator(sys.argv[1])
p.findPhilosophy()