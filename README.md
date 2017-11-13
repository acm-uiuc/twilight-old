# Twilight
Root repo for twilight

## Overview 

[twilight-hardware](https://github.com/acm-uiuc/twilight-hardware)

[twilight-embedded](https://github.com/acm-uiuc/twilight-embedded)

[twilight-ios](https://github.com/acm-uiuc/twilight-ios)

[twilight-border-router](https://github.com/acm-uiuc/twilight-border-router)


## Getting Started

Make sure you have Python and pip installed before starting 

There are a couple components of the twilight. To get all of them we use a tool called repo 

1. Install repo - https://android.googlesource.com/tools/repo/

    Mac OS
    ```sh
    brew install repo 
    ```

    Ubuntu 14.04+
    ```sh    
    sudo apt install repo

    ```
2. Make a directory to house your twilight work
    ```sh
    mkdir twilight
    ```
    
3. Within this directory run the following command to start managing the projects

    ```sh    
    repo init -u git@github.com:acm-uiuc/twilight
    ```
    
4. Run the following command to grab the latest of all the repos 

    ```sh    
    repo sync
    ```
