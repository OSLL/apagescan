# _apagescan_
### Welcome to our project! 

[Operating System Laboratory](http://project2043696.tilda.ws/page9393990.html) introduce a new tool - _apagescan_ for virtual memory page tracking. _apagescan_ maintain:

1. Graphical user-friendly interface
2. Display information page by page
3. Display process tree
4. Selection of processes from cgroups
5. Scanning zRAM 

> TBD - link on publication - somewhere

## Table of contents
* [Installation](#Installation)

* [Usage](#Usage)

* [Contributing](#Contributing)

## Installation

### Requirements

*  [_adb_ - Android Debug Bridge](https://developer.android.com/studio/command-line/adb)
*  gcc-arm
* Python 3.6+:
  * pip3
  * virtualenv

On Ubuntu run:

   ```bash
 sudo apt-get install android-tools-adb android-tools-fastboot
 sudo apt install gcc-arm-linux-gnueabi
 pip3 install virtualenv
   ```
### Get Started

#### Installing on Ubuntu 18.04. 

Open terminal and follow these steps:

1. Clone this repo:
    ```bash
    git clone https://github.com/OSLL/apagescan.git
    ```
    
2. Change directory to `apagescan`:

    ```bash
    cd apagescan/
    ```

3. > TBD add info how to compile and move .c files to device

4. Set up the environment and install tool:

    ```bash
    ./setup.sh
    ```
## Usage

### Start
Make sure that your **device is unlocked** and you have **root privileges**. 

0. Connect your device and run in terminal:

   ```bash
    adb root
   ```
1. Run the `apagescan`

### Example usage

TBD

**_NOTE_**: The full interface description you can find on [Wiki](https://github.com/OSLL/apagescan/wiki/Interface-guide)

## Contributing
Contributions are welcome, and they are greatly appreciated! 
Report bugs at https://github.com/OSLL/apagescan/issues.
If you are reporting a bug, please apply label "bug" and  include:

* Any details about your local setup that might be helpful in troubleshooting;
* Detailed steps to reproduce the bug.

