# Peristéri (Perist-ri)
Submit to Themis through command line and get Themis's feedback.

Successful submission attempt:
    ![][overview]

Failed submission attempt:
    ![][failed]

## Requirements
1. Git
    > [windows](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/#:~:text=Installing%20on%20Windows)

    > [mac](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#:~:text=com/download/linux.-,Installing%20on%20macOS,-There%20are%20several)

    > [Linux](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#:~:text=work%20just%20fine.-,Installing%20on%20Linux,-If%20you%20want)

2. Python
    > installation guide [here](https://realpython.com/installing-python/)

## Installation

    > git clone git@github.com:Stylo2k/Perist-ri.git
    > sh install


## First time configuration
For the first time configuration you will need to specify your student number (with a lower case s) and your password
This data will get stored locally in :

    ~/.themis_submitter/data.yaml

## Usage

### Through command line arguments
    > python Peristéri.py \<file to submit> \<submission url>
This will simply submit your file to the url you specify. This is the cleanest way to submit. But since not all people will prefer this way. You can use the browser method.

### As a command line browser
    > python Peristéri.py
This will let you browse Themis just like you would in your browser. BUT of course through the terminal.

You can specify to what directory you want to go with numbers (indices). When you are at a submittable page, you will get asked if you want to submit or go back. When you submit a small window will open to get you to choose the file you want to submit.

### After submission

After submission your submitted file wil get judged and the test cases you passed/failed will get prompted in your terminal. If you pass all test cases the program will terminate. Otherwise, you are given the chance to resubmit.

# Coming features
1. See in, out & difference test files
2. Get hints from failed test cases
3. ?

[overview]: resources/Screenshot.png "alt"
[failed]: resources/failed.png