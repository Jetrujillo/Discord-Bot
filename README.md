# Discord-Bot

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Fun little project of creating a discord bot based off of discord.py.

For the purpose of making the bot easy to work on any system, I am packaging it in a Docker container.

Eventually this will be converted to work with Discord's "slash commands" outlined [here](https://blog.discord.com/slash-commands-are-here-8db0a385d9e6).


<!-- GETTING STARTED -->
## Getting Started

My project involves Docker (version 20.10.8) and running CentOS7. For the purpose of these steps, I will assume you will use CentOS 7.

You can folllow [this link](https://docs.docker.com/engine/install/) to installing docker on your choice of system.

### Prerequisites

  Assuming you have CentOS 7 available, you will need to install Docker and git.
  
* [Docker](https://docs.docker.com/engine/install/centos/)
* Git
   ```sh
   sudo yum install git
   ```
  

### Installation

1. Clone the repo
   ```sh
   git clone git://github.com/Jetrujillo/Discord-Bot.git
   ```
2. Step into the Discord-Bot project folder
   ```sh
   cd Discord-Bot/_Discord-Bot_1.0/
   ```
3. Build the docker image
   ```sh
   sudo docker build --tag python-dbot .
   ```
4. Run the Docker Container
   ```sh
   sudo docker run -d --shm-size=1024m python-dbot
   ```


<!-- USAGE EXAMPLES -->
## Usage

TBD


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()
