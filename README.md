# conan-SimpleAmqpClient

[Conan.io](https://conan.io) package for [SimpleAmqpClient library](https://github.com/alanxz/SimpleAmqpClient)

| Appveyor | Travis |
|-----------|--------|
|[![Build Status](https://ci.appveyor.com/api/projects/status/github/db4/conan-SimpleAmqpClient?branch=master&svg=true)](https://ci.appveyor.com/project/db4/conan-SimpleAmqpClient)|[![Build Status](https://travis-ci.org/db4/conan-SimpleAmqpClient.svg?branch=master)](https://travis-ci.org/db4/conan-SimpleAmqpClient)|

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload conan-SimpleAmqpClient/2.5.0-pre1@dbely/stable --all

## Reuse the packages

### Basic setup

    $ conan install conan-SimpleAmqpClient/2.5.0-pre2@dbely/stable

### Project setup

If you handle multiple dependencies in your project, it would be better to add a *conanfile.txt*

    [requires]
    conan-SimpleAmqpClient/2.5.0-pre2@dbely/stable

    [generators]
    txt
    cmake


