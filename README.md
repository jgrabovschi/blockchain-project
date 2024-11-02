> [!WARNING]
> This is only an academic prototype.

# Blockchain Project

This is a blockchain platform that I made to learn how the blockchains work and to make a lighter application. It implements many blockchain mechanisms and it uses the PoA consensus algorithm.

The code that I made is working for the the following topology:

![cenario-testes-1](https://github.com/user-attachments/assets/26fcf20d-c2cf-47b6-99f7-7ff12fa16aaa)

## Installing

> [!CAUTION]
> You need to do this on all of the nodes in the blockchain network.
 
 Here are the instructions:

```
git clone https://github.com/jgrabovschi/blockchain-project
cd blockchain-project
```
Then you need to edit the *main* file to use the node's IP address:

```
# vi main
HOST = "10.0.1.1"
```

## Usage
### Nodes
Now you only need to run the *main* script, it will prompt a message asking if you want to create or load an existing blockchain:

```
./main
Do you want to create a new blockchain or load an existing one? (new/load)
>
```
You need to type *new* or *load*

### Client
To send data to the blockchain you only need to run the *client* script:

```
./client
```

> [!NOTE]
> This project also comes with a bad client if you want to test it.

## Demo

You can watch a demo of this project [here](https://www.youtube.com/watch?v=wvKM2mQaUQc&t=1s&ab_channel=JorgeGrabovschi).

## Main Issues and Challenges

- The algorithm and password to create the signature is exposed on this repo, so it's not that secure.
- You need to run all of the nodes that are on the HOSTS array (in the *client*, *client-bad* and *synch.py* files), it won't work correctly if you don't. That is because the platform doesn't have a Node Discovery algorithm.
