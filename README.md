# FastCopy

## What is FastCopy?

FastCopy is tool to help users copy large files from one harddrive to another. Some use cases include large csv and database files on the magnitude of Terabytes. If you just try to copy and paste a file from one harddrive to another you'll notice that it'll take an enormous amount of time and if you try to do other tasks on your computer it will seem impossible and laggy. This is because when you copy files on your computer it will by default use buffered I/O which means it will put everything that you want to copy and put it into memory before actually copying it to its destination.

FastCopy is just a program that uses overlapped unbuffered I/O from one harddrive to another. It will bypass putting anything into memory. This means that other programs running on the same computer will no longer have to load everything back into memory when it is its turn on the CPU.

## Current Limitations

FastCopy is not restartable at the moment. Meaning that if your computer crashes or the destination computer crashes during copying it will not be able to restart at the point where it crashed.
