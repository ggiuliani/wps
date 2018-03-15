#wps.des: id = swatSUB, title = Processing of SWAT output.sub data, abstract = Generates text files for each SWAT variable;
#wps.in: id = var_outputsub, type = string, title = Path to output.sub, abstract = Path to the output.sub file;
#wps.in: id = var_legend, type = string, title = Path to legend, abstract = Path to legend file;
var_outputsub<-"/home/greg/R/output.sub"
var_legend<-"/home/greg/R/legend.csv"

library("foreign")
Qs1<-read.table(var_outputsub,skip=9)

textfile<-readLines(file(var_outputsub))
write.dbf(textfile[9],"legend.dbf")

legend_names<-read.table(var_legend,sep=",")

for (i in 5:25){
datafile<-Qs1[,c(2,i)]
colnames(datafile)=c(as.character(legend_names[1,1]),as.character(legend_names[1,i]))
write.dbf(datafile,paste("/home/greg/Desktop/Routput/",substr(legend_names[1,i], 1, 5),".dbf",sep=""))
}
