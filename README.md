# Markovstuck
Markovstuck is a web application that generates Homestuck pages using Markov chains. It is inspired by [/r/subredditsimulator](http://www.reddit.com/r/subredditsimulator) subreddit on Reddit and [Headline Smasher](http://www.headlinesmasher.com).

You can use a live copy of this site at [markovstuck.matoking.com](http://markovstuck.matoking.com).

# Installation
The Python dependencies for this project are in the file requirements.txt and they can be installed by running the following command:

```
pip install -r requirements.txt
```

In addition to usual requirements for a Django application, Markovstuck also requires a Redis server acting as a persistent storage (check the 'persistent' cache in settings.py).

Before any pages can be generated, you'll need to run two commands to download and parse data from MSPAdventures.com the web application uses to create its Markov models:

```
python manage.py update_data
python manage.py update_images
```

To ensure that pages can be generated fast, you need to run the provided chain_server.py script, which loads every existing Markov chain into memory at once. At the time of writing, the server consumes about ~500 MB of RAM once loaded.

```
python chain_server.py
```


# Donations
BTC: 1DL3LxGZ5ratGSmkL8VD2Tp9vd8aD1Argu

# Disclaimer
Homestuck is owned by MSPAdventures.com. This web application is neither affiliated with or endorsed by MSPAdventures.com.

# License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
