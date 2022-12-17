# Underground chat

To connect to the underground chat.

### How to install
Python3 should be already installed.

1) clone the repo
2) install dependencies:
    ```
    pip install -r requirements.txt
    ```
   
3) add .env file in the directory of the project:
    ```
    HOST=<host>
    READ_PORT=<port>
    WRITE_PORT=<port>
    HISTORY_FILE=<path_to_file_with_chat_history>
    DEVMAN_TOKEN=<token>
    ```
4) add file to the dicrectory of the project to write history 

### How to use
1) Write to the chat: 
    ```
    python3 sender.py --message=<message>
    ```
2) Read the chat: 
    ```
    python3 receiver.py
    ```
3) if you want to overwrite settings to write to the chat for the current conncection, you can use arguments:
    ```
    --host=<host>
    --write_port=<port>
    --token=<token>
    ```

3) if you want to overwrite settings to read the chat for the current conncection, you can use arguments:
    ```
    --host=<host>
    --port=<port>
    --history=<path_to_file_with_chat_history>
    ```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
