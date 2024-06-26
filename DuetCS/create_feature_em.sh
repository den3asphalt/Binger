export CLASSPATH=".:antlr-4.13.1-complete.jar:$CLASSPATH"
alias grun='java -Xmx500M -cp "antlr-4.13.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

for f in ` ls $1 `
do
        f=$1"/"$f
        file=$f
        if [ "${file##*.}"x = "js"x ];then
                grun JavaScript program -tree $file > testjs.txt
                s="JavaScript"
        elif [ "${file##*.}"x = "java"x ];then
                grun Java8 compilationUnit -tree $file > testj8.txt
                s="Java8"
        elif [ "${file##*.}"x = "cpp"x ];then
                grun CPP14 translationunit -tree $file > testc14.txt
                s="CPP14"
        fi
        echo $f 
        echo $s
        #python3 data_prepare.py $1
	python3 feature.py $f $s
    
done


