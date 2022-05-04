<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@200;600&display=swap');
body{
font-family: 'Source Code Pro', monospace;
}
h1, h2, h3{
font-weight: bold;
}
p{
font-size: 1.1rem;
}
span{
font-weight: bold;
color: green;
}
.subtitle {
font-weight: bold;
}
</style>

<div style="width:100%;">
  <pre align="center" style="margin-bottom:-37px;">██████╗ ██╗   ██╗██╗     ███████╗███████╗██████╗ </pre>
  <pre align="center" style="margin-bottom:-37px;">██╔══██╗╚██╗ ██╔╝██║     ██╔════╝██╔════╝██╔══██╗</pre>
  <pre align="center" style="margin-bottom:-37px;">██████╔╝ ╚████╔╝ ██║     █████╗  █████╗  ██████╔╝</pre>
  <pre align="center" style="margin-bottom:-37px;">██╔═══╝   ╚██╔╝  ██║     ██╔══╝  ██╔══╝  ██╔══██╗</pre>
  <pre align="center" style="margin-bottom:-37px;">██║        ██║   ███████╗██║     ███████╗██║  ██║</pre>
  <pre align="center" style="margin-bottom:-37px;">╚═╝        ╚═╝   ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝</pre>
</div>

<h1 align="center" style="margin-top: 37px;">Share all you want on a P2P connection!</h1>
<br>
<h2>Requirements:<h2>
<p><span>tqdm</span></p>
<p><span>windows-curses</span> (Optional, if using windows)</p>
<br>
<h2>The <span>help</span> command:</h2>

```console
help

  banner: Shows a pretty random banner.

  set: Changes an option before the connection. You can change:

           mode: client/server
           ip: ip to connect to as a client. Can be equal to 'localhost' or 'locip' for automated ip assignment.
           ipmode: ipv4/ipv6 changes automatically if you specify an ip address.
           port: port to set up the connection.
           upnp: on/off enables upnp port forwarding.
           whitelist: on/off allows only specified ips to connect to your server.
           blacklist: on/off prevents the specified ips to connect to your server.

  show: Shows the values of each option. You can specify a particular option to only show that value (more detail).
  show locip: Shows your local ip.


  FILE LIST: As a server, this is the list of files that will be available for download.
             If left empty, the server will start as a chat server.
             As a client, this is the list of files you will request to the server for download.
             You can leave it empty and use 'show sfiles' command after the connection to select wich files to download.

  file add: Adds a file to the file list.
  file allfilesin: Adds all files from a directory to the file list.
  file remove: Removes a file from the file list.
  file removen: Removes a file from the file list by its index number.
  file clear: Erases all contents from the file list.


  WHITELIST: Its only used in server mode. Its the list of ips that are allowed to connect to the server. Its not obligatory.
             It doesnt work if the whitelist parameter is not set to true ('set whitelist true')

  whitelist add: Adds an ip to the whitelist.
  whitelist remove: Removes an ip from the whitelist.
  whitelist removen: Removes an ip from the whitelist by its index number.
  whitelist clear: Erases all contents from the whitelist.


  BLACKLIST: Its only used in server mode. Its the list of ips that are not allowed to connect to the server. Its not obligatory.
             It doesnt work if the blacklist parameter is not set to true ('set blacklist true')

  blacklist add: Adds an ip to the blacklist.
  blacklist remove: Removes an ip from the blacklist.
  blacklist removen: Removes an ip from the blacklist by its index number.
  blacklist clear: Erases all contents from the blacklist.


  fire: executes the connection with the chosen options.

  exit: Closes the program.
```

<br>
<h2>Setting up a server:</h2>
<p>First we set the mode to server:</p>

```console
> set mode server
```

<p>And the ip to our local ip:</p>

```console
> set ip locip
```

<p>You can always check the current configuration to see if it worked with <span>show</span>:</p>

```console
> show

        mode:  server
        ip:  192.168.0.225
        ipmode:  IPv4
        port:  4444
        upnp:  False
        whitelist:  False
        blacklist:  False
```

<h3>Configuring whitelist/blacklist:</h3>
Whitelist and blacklist commands are configured the same way. Both are optional.
<p class="subtitle">Adding an ip to the list:</p>

```console
> whitelist add 127.0.0.1
```

Check the list with <span>show whitelist</span> or <span>show blacklist</span>:

```console
> show whitelist

  whitelist status:  False

  [0]   127.0.0.1
```

<p class="subtitle">Enabling witelist/blacklist:</p>
<p>Pylfer wont filter the clients ip if you don't enable the use of the lists.</p>

```console
> set whitelist true
```

<p class="subtitle">Removing an ip from a whitelist/blacklist:</p>
<p>You can remove it by typing the entire ip, or by the index number that shows when you use the <span>show whitelist</span> or <span>show blacklist</span> command.</p>

```console
 > show whitelist

  whitelist status:  True

  [0]   127.0.0.1

 > whitelist removen 0
 > show whitelist

  whitelist status:  True
```

<h3>Setting up a file server:</h3>
If we want to create a file server, now we add the files:

```console
> file add "C:/Test.jpg"
> file allfilesin "C:/Music/Clasic"
```

You can always check your file list using <span>show files</span>:

```console
 > show files

  [0]   C:/Test.jpg
  [1]   C:/Music/Clasic/Antonio Vivaldi - The Four Seasons - Summer.mp3
  [2]   C:/Music/Clasic/Antonio Vivaldi - The Four Seasons - Winter.mp3
  [3]   C:/Music/Clasic/Beethoven - 7th Symphony.mp3
  [4]   C:/Music/Clasic/Chopin - Nocturnes.m4a
  [5]   C:/Music/Clasic/Debussy - Arabesque No-1.mp3
  [6]   C:/Music/Clasic/Strauss - Also sprach Zarathustra - Dudamel.mp3
  [7]   C:/Music/Clasic/Symphony No. 9 - Beethoven.mp3
```

The numbers that appear in brackets are the index numbers, you can use this to delete files from your list without typing the entire name:

```console
> file removen 0
> show files

  [0]   C:/Music/Clasic/Antonio Vivaldi - The Four Seasons - Summer.mp3
  [1]   C:/Music/Clasic/Antonio Vivaldi - The Four Seasons - Winter.mp3
  [2]   C:/Music/Clasic/Beethoven - 7th Symphony.mp3
  [3]   C:/Music/Clasic/Chopin - Nocturnes.m4a
  [4]   C:/Music/Clasic/Debussy - Arabesque No-1.mp3
  [5]   C:/Music/Clasic/Strauss - Also sprach Zarathustra - Dudamel.mp3
  [6]   C:/Music/Clasic/Symphony No. 9 - Beethoven.mp3
```

Finally we launch the server:

```console
> fire

  Listening on port 4444 ...
```

<h3>Setting up a chat server:</h3>
A chat server is even easier than a file server. All you need is an empty file list.
<p>(after configuring your ip to locip, your port number and whitelist/blacklist)</p>

```console
> show files

File list is empty.
```

Launching with:

```console
> fire

  Listening on port 4444 ...
```

<br>
<h2>Connecting to a server:</h2>
To connect to a server as a client first you must know the server ip and port numbers.

```console
> set ip 127.0.0.1
> set port 12345
```

Then we connect:

```console
> fire
```

<p class="subtitle">If we connected to a chat server:</p>
Then you will see this text:

```console
> fire


  Connection established!

  Username:
```

Now you have to type a username, this username will appear when you chat. And that's it, you can chat now!
<p class="subtitle">If we connected to a file server: </p>
Then you will see something like this:

```console
 > fire


  Connection established!


  There are 7 files available for download.
  Receiving the file list...
  Done.


 >>
```

The double greater-than sign indicates that you are connected to the server. Now you can throw commands to communicate with it.

```console
>> help

  file add: Adds a file to the download list.
  file addn: Adds a file to the download list by its index number.
  file remove: Removes a file from the download list.
  file removen: Removes a file from the download list by its index number.
  file clear: Erases all the contents from the download list.
  all files: Adds all the available files to de download list.
  * There is no distinction between file and files commands...

  show  files: Shows the files in your download list
  show sfiles: Shows the files that the server has available for download.

  update: Updates the server file list.

  download: Starts the download of the chosen files in your download list.
              ** If the list is empty, downloads everything from the server!

  disconnect: Ends the connection with the server.

  exit: Closes the program.
```

First command we should use is <span>show sfiles</span> this will show the files the server has for download

```console
>> show sfiles

  [0]   Antonio Vivaldi - The Four Seasons - Summer.mp3
  [1]   Antonio Vivaldi - The Four Seasons - Winter.mp3
  [2]   Beethoven - 7th Symphony.mp3
  [3]   Chopin - Nocturnes.m4a
  [4]   Debussy - Arabesque No-1.mp3
  [5]   Strauss - Also sprach Zarathustra - Dudamel.mp3
  [6]   Symphony No. 9 - Beethoven.mp3
```

Now we add the files we want to download to our download list. Note that we have an index number for each file, so using <span>file addn</span> is usually faster than <span>file add</span>.
If the download list is empty, then we will download all the files.

```console
>> show files

  File list is empty. (Download everything mode)

 >> file addn 0 3 4
 >> show files

  [0]   Antonio Vivaldi - The Four Seasons - Summer.mp3
  [1]   Chopin - Nocturnes.m4a
  [2]   Debussy - Arabesque No-1.mp3

```

Now we are ready for download:

```console
>> download
  Starting download...

  Downloading Antonio Vivaldi - The Four Seasons - Summer.mp3: 100%|██████████████| 14.4M/14.4M [00:01<00:00, 13.9MB/s]
  Done.

  Downloading Chopin - Nocturnes.m4a: 100%|█████████████████████████████████████████| 154M/154M [00:01<00:00, 89.7MB/s]
  Done.

  Downloading Debussy - Arabesque No-1.mp3: 100%|█████████████████████████████████| 6.05M/6.05M [00:01<00:00, 5.35MB/s]
  Done.

 >
```

Note that when download is complete we are disconnected from the server (we have a single greater-than sign).