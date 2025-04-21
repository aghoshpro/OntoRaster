# Technical Issues and Fixes

### Java Installation in Ubuntu [1,2,3,4]

```sh
apt search openjdk

sudo apt install openjdk-21-jdk openjdk-21

sudo apt-get update

export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 && export PATH=$PATH:$JAVA_HOME/bin
```

```
$ java -version

> openjdk version "11.0.25" 2024-10-15
> OpenJDK Runtime Environment (build 11.0.25+9-post-Ubuntu-1ubuntu120.04)
> OpenJDK 64-Bit Server VM (build 11.0.25+9-post-Ubuntu-1ubuntu120.04, mixed mode, sharing)

```

```
$ echo $JAVA_HOME

echo $JAVA_HOME
usr/lib/jvm/java-11-openjdk-amd64
```

### SPARQLWrapper QueryBadFormed Error for long SELECT query [10, 11]

### StackOverflow

1. <https://askubuntu.com/questions/277806/how-to-set-java-home/1385764#1385764>
2. <https://stackoverflow.com/questions/60065441/java-home-variable-issues>
3. <https://stackoverflow.com/questions/14788345/how-to-install-the-jdk-on-ubuntu-linux>
4. <https://stackoverflow.com/questions/21343529/all-my-java-applications-now-throw-a-java-awt-headlessexception>
5. <https://stackoverflow.com/questions/42045767/how-can-i-change-the-x-axis-so-there-is-no-white-space/42045987#42045987>
6. <https://stackoverflow.com/questions/69886690/remove-empty-space-from-matplotlib-bar-plot>
7. <https://stackoverflow.com/questions/65104927/add-text-to-folium-map-using-an-absolute-position>
8. <https://stackoverflow.com/questions/3346396/in-semantic-web-are-owl-el-rl-ql-all-instances-of-dl-what-is-the-difference>
9. <https://stackoverflow.com/questions/24817607/why-must-rdfdatatype-subclass-rdfclass-in-rdf>
10. <https://github.com/RDFLib/sparqlwrapper/issues/124>
11. <https://sparqlwrapper.readthedocs.io/en/latest/main.html>
