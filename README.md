# _apagescan_
### Welcome to our project! 

[Operating System Laboratory](http://project2043696.tilda.ws/page9393990.html) introduce a new tool - _apagescan_ for virtual memory page tracking.

_apagescan_ maintain:

1. Graphical user-friendly interface
2. Display information page by page
3. Display process tree
4. Selection of processes from cgroups
5. Scanning zRAM 

## Table of contents
[Installation](#Installation)

[Usage](#Usage)

[Contributing](#Contributing)

## Installation

### Requirements

* [Adb - Android Debug Bridge](https://developer.android.com/studio/command-line/adb)
* Cross compiler to arm
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

3. Connect your device (**must be rooted and unlocked**)

    ```bash
    cd tool/
    make
    ```

4. Set up the environment and install tool:

    ```bash
    cd ../
    ./setup.sh
    ```
## Usage

### Start
0. Connect your device and run in terminal (optional):

   ```bash
    adb root
   ```
   
1. Run the `apagescan`

### Example usage
1. Choose PIDs  


![image](https://user-images.githubusercontent.com/29632527/76162701-4d93d280-6151-11ea-8429-bdb561c6e88c.png)  


2. Push `Collect Data` button and set time-interval: 10-sec. experiment with 0 sec. delay between data collection  


![image](https://user-images.githubusercontent.com/29632527/76162795-d448af80-6151-11ea-816f-79a32a7c0628.png)  


3. Watch the result  


![image](https://user-images.githubusercontent.com/29632527/76162822-0d811f80-6152-11ea-8ddc-ffd2ed9f8420.png)



**_NOTE_**: The full interface description you can find on [Wiki](https://github.com/OSLL/apagescan/wiki/Interface-guide)

## Contributing
Contributions are welcome, and they are greatly appreciated! 
Report bugs at https://github.com/OSLL/apagescan/issues.
If you are reporting a bug, please apply label "bug" and  include:

* Any details about your local setup that might be helpful in troubleshooting;
* Detailed steps to reproduce the bug.

