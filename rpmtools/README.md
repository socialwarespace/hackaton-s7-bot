# rpmtools

Этот репозиторий содержит скрипты/шаблоны, упрощающие создание rpm

Поддерживаемые технологии:

* Python
* Node
* Yii

Также существует simple-сборка, которая упаковывает в пакет 
содержимое папки public, которая находится в корне проекта. 
Перед созданием пакета выполняется:

* Запуск npm install, если имеется файл package.json,
* Запуск bower install, если имеется файл bower.json,
* grunt, если имеется файл Gruntfile.js

### Simple

В пакет попадут все файлы после сборки из папки public, которая находится в корне проекта.
После установки файлы находятся в /opt/<имя пакета>

##### Параметры

* -b --build - номер релиза. По-умолчанию текущий timestamp
* -g --grunttask - название grunt-таска, который будет запускаться в процессе сборки. По-умолчанию default

##### Сборка

1. Создать в корне проекта файл package.json. Указать name, version
2. Запустить из корня проекта ./rpmbuild/simple/build.sh

### Python

После установки файлы находятся в /opt/<имя пакета>

##### Параметры

* -b --build - номер релиза. По-умолчанию текущий timestamp
* -v --virtualenv - путь до virtualenv, с которым будет произведена сборка. По-умолчанию вывод команды ```which virtualenv``` 

##### Параметры package.json

* name - имя проекта
* version - версия проекта
* description - описание проекта
* yumDependencies — зависимости (опционально)
* yumBuildDependencies - зависимости сборки (опционально)
* requirementsPath — путь до requirements.txt (опционально)
* requirementsContentCommand — команда, которая возвращает содержимое requirements.txt. Используется для инвалидации кеша сборки (опционально)
* gruntCwd - переход в директорию с grunt-скриптом (опционально)
* excludeFiles — файлы, которые не нужно помещать в пакет (опционально)
* virtualenv — путь до virtualenv и ключи запуска (опционально)
* buildCmds — команды сборки (опционально) 
* afterInstallCmd — команда после установки пакета 
* template — шаблон сборки, упаковывает стандартные конфиги и скрипты. Значения: django, supervisor (опционально)

 
##### Сборка

1. Создать в корне проекта папку build, в ней создать package.json. Указать name, version, yumDependencies (массив), yumBuildDependencies (массив)
2. Запустить из корня проекта ./rpmbuild/tornado/build.sh
3. После установки пакета в конфиге по-умолчанию /etc/<имя пакета>/supervisord.conf необходимо скорректировать номер процесса

### Yii, Node

Under construction