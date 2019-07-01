# PackWithoutLack -- JAVASCRIPT-IMPLEMENTATION BRANCH

__The purpose of this branch is to turn PackWithoutLack.py into an API which will be called from a javascript file which is acting as a pretty front-end for the user to interact with. :)__




___

PackWithoutLack means that the next time you go to pack your bag before you leave you won't be lacking anything you need.

It doesn't matter if you're packing the bag for just this afternoon, the weekend or any anyother amount of time up to 8 days, PackWithoutLack has you covered.

## Instructions

It couldn't be easier (that is until the javascript is working)

1. run the command 

    ```
    python PackWithoutLack.py
    ```

2. Enter the postcode of where you are going as one word 

    ```
    Postcode: HS33HL
    ```

3. Enter how many days (and how many hours if prompted) as a number

4. Bingo Bango Bongo, Bish Bash Bosh you have been given what you need to pack

### BoulderJudgment

This new feature not not only means that PackWithoutLack tells you what to pack but will tell you what the conditions for bouldering are at the supplied postcode, with absolutly no extra input from you!

​																	**GO CHECK IT OUT NOW!!!!**


Instructions for setting up python server:
1. Go to packwithoutlack folder and create virtual environemnt by typing
```
virtualenv myProject
```
2. Activate the virtual environment
```
//MacOSX/Linux
source myProject/bin/activate
//Windows
myproject\Scripts\activate
```
3. Install flask in you source
```
pip install flask
pip install -U flask-cors
```
4. Run packwithoutlack.py
```
python packwithoutlack.py
```
5. Pass parameters by going to http://127.0.0.1:5000/ and adding defualt/param1/param2/param3

_Works best on OSX for current terminal output formatting_
_Also requires to be run as python 2.7 or any other python 2.x package_

Hosting website: https://pages.github.com/
