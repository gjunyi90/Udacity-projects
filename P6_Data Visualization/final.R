library(ggplot2)
library(dplyr)
library(gridExtra)

#http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time

dfsum<-read.csv('df10_16.csv', sep = ',')

############################################################################

dfsum[is.na(dfsum)] <- 0



dfsum1 <- dfsum %>%
  group_by(YEAR,UNIQUE_CARRIER) %>%
  summarize(ARR = length(ARR_DEL15),
            DELARR = sum(ARR_DEL15),
            DEP = length(DEP_DEL15),
            DELDEP = sum(DEP_DEL15),
            DIV = sum(DIVERTED)) %>%
  transform(PUNCTUALARR = 1 - DELARR/ARR)%>%
  transform(PUNCTUALDEP = 1 - DELDEP/DEP)



############################################################################

plot1 <- ggplot(data = dfsum1,
       aes(x = YEAR, y = PUNCTUALARR)) +
  geom_line(aes(color = UNIQUE_CARRIER))+
  geom_line(fun.y = mean, stat='summary', linetype=6)+
  scale_y_continuous(name="PUNCTUALITY", limits=c(0.7, 1))

plot2 <- ggplot(data = dfsum1,
       aes(x = YEAR, y = PUNCTUALDEP)) +
  geom_line(aes(color = UNIQUE_CARRIER))+
  geom_line(fun.y = mean, stat='summary', linetype=6)+
  scale_y_continuous(name="PUNCTUALITY", limits=c(0.7, 1))

grid.arrange(plot1, plot2 ,nrow=1)


levels(dfsum1$UNIQUE_CARRIER)

#Average Punctuality, Grouped by carrier
AGGARR <- dfsum1 %>%
  group_by(UNIQUE_CARRIER) %>%
  summarize(ANNUALAVGARR = mean(PUNCTUALARR))

AGGDEP <- dfsum1 %>%
  group_by(UNIQUE_CARRIER) %>%
  summarize(ANNUALAVGDEP = mean(PUNCTUALDEP))

# Top 25% for Puntuality
TOPPUNCTUALITYARR <- subset(AGGARR, ANNUALAVGARR >= quantile(ANNUALAVGARR, 0.75))$UNIQUE_CARRIER
TOPPUNCTUALITYDEP <- subset(AGGDEP, ANNUALAVGDEP >= quantile(ANNUALAVGDEP, 0.75))$UNIQUE_CARRIER

# Bottom 25% for Puntuality
BOTPUNCTUALITYARR <- subset(AGGARR, ANNUALAVGARR <= quantile(ANNUALAVGARR, 0.25))$UNIQUE_CARRIER
BOTPUNCTUALITYDEP <- subset(AGGDEP, ANNUALAVGDEP <= quantile(ANNUALAVGDEP, 0.25))$UNIQUE_CARRIER

#Filter by TOPPUNCTUALITYARR as some year there are new or missing airlines
dfsum2 <- subset(dfsum, is.element(UNIQUE_CARRIER, TOPPUNCTUALITYARR)) %>%
  group_by(YEAR, UNIQUE_CARRIER) %>%
  summarize(ARR = length(ARR_DEL15),
            DEP = length(DEP_DEL15),
            DELDEP = sum(DEP_DEL15),
            DELARR = sum(ARR_DEL15)) %>%
  transform(PUNCTUALITYARR = 1 - DELARR/ARR)%>%
  transform(PUNCTUALITYDEP = 1 - DELDEP/DEP)

dfsum3 <- subset(dfsum, is.element(UNIQUE_CARRIER, BOTPUNCTUALITYARR)) %>%
  group_by(YEAR, UNIQUE_CARRIER) %>%
  summarize(ARR = length(ARR_DEL15),
            DEP = length(DEP_DEL15),
            DELDEP = sum(DEP_DEL15),
            DELARR = sum(ARR_DEL15)) %>%
  transform(PUNCTUALITYARR = 1 - DELARR/ARR) %>%
  transform(PUNCTUALITYDEP = 1 - DELDEP/DEP)


PLOTARR <- ggplot(data = dfsum2,
                  aes(x = YEAR, y = PUNCTUALITYARR)) +
  geom_line(aes(color = UNIQUE_CARRIER)) +
  scale_x_continuous(limits=c(2010, 2016), breaks=c(2010:2016))

PLOTDEP <- ggplot(data = dfsum2,
                  aes(x = YEAR, y = PUNCTUALITYDEP)) +
  geom_line(aes(color = UNIQUE_CARRIER)) +
  scale_x_continuous(limits=c(2010, 2016), breaks=c(2010:2016))

PLOTARR2 <- ggplot(data = dfsum3,
                  aes(x = YEAR, y = PUNCTUALITYARR)) +
  geom_line(aes(color = UNIQUE_CARRIER)) +
  scale_x_continuous(limits=c(2010, 2016), breaks=c(2010:2016))

PLOTDEP2 <- ggplot(data = dfsum3,
                  aes(x = YEAR, y = PUNCTUALITYDEP)) +
  geom_line(aes(color = UNIQUE_CARRIER)) +
  scale_x_continuous(limits=c(2010, 2016), breaks=c(2010:2016))


grid.arrange(PLOTARR, PLOTDEP,PLOTARR2, PLOTDEP2 ,ncol=2)

write.csv(dfsum2, file="data3a.csv", row.names=FALSE)
write.csv(dfsum3, file="data3b.csv", row.names=FALSE)


