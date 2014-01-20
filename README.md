![Kickflip!](http://24.media.tumblr.com/tumblr_m92dqeIJe11r28y0mo1_500.gif)
# python-kickflip

It's a Kickflip library and command line client!

## Command Line Usage

0. First, you'll need a [Kickflip](http://kickflip.io) account and an application.

0. Install *kickflip*

    ```python
    pip install kickflip
    ```

0. Stream away!

    ```python
    kickflip MyVideo.mp4
    ```

0. The first time you run kickflip, it'll ask for you application's keys. These will be stored for future usage. They can also be set any time with the *-k* argument.

    ```
    What is your client ID? my_client_ID
    What is your client secret? my_client_secret
    ```

## Library Usage

python-kickflip can also be used as a library for your python applications.

1. First, import kickflip.

    ```python
    import kickflip
    ```
2. Then, set up and stream away!

    ```python
    kickflip.set_keys(client_id, client_secret)
    kickflip.set_user(user)
    stream = kickflip.start_stream(file_path)
    ```
