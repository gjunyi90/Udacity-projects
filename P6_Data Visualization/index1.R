library(ggplot2)
library(dplyr)
library(gridExtra)

#http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time

dfsum<-read.csv('df10_16.csv', sep = ',')

############################################################################

#Remove all the 
dfsum[is.na(dfsum)] <- 0

dfsum1 <- dfsum %>%
  group_by(YEAR,UNIQUE_CARRIER) %>%
  summarize(ARR = length(ARR_DEL15),
            DELARR = sum(ARR_DEL15),
            DEP = length(DEP_DEL15),
            DELDEP = sum(DEP_DEL15),
            DIV = sum(DIVERTED)) %>%
  transform(PUNCTUAL = 1 - DELARR/ARR)


############################################################################

ggplot(data = dfsum1,
       aes(x = YEAR, y = PUNCTUAL)) +
  geom_line(aes(color = UNIQUE_CARRIER))+
  scale_y_continuous(name="PUNCTUALITY", limits=c(0.7, 1))

#Average Punctuality, Grouped by carrier
AGGARR <- dfsum1 %>%
  group_by(UNIQUE_CARRIER) %>%
  summarize(ANNUALAVGARR = mean(PUNCTUAL))

# Top 25% of Carriers
TOPPUNCTUALITY <- subset(AGGARR, ANNUALAVGARR >= quantile(ANNUALAVGARR, 0.75))$UNIQUE_CARRIER

dfsum2 <- subset(dfsum, is.element(UNIQUE_CARRIER, TOPPUNCTUALITY)) %>%
  group_by(YEAR, UNIQUE_CARRIER) %>%
  summarize(ARR = length(ARR_DEL15),
            DEP = length(DEP_DEL15),
            DELDEP = sum(DEP_DEL15),
            DELARR = sum(ARR_DEL15)) %>%
  transform(PUNCTUALITYARR = 1 - DELARR/ARR)%>%
  transform(PUNCTUALITYDEP = 1 - DELDEP/DEP)

ggplot(data = dfsum2,
       aes(x = YEAR, y = PUNCTUALITYARR)) +
  geom_line(aes(color = UNIQUE_CARRIER)) +
  scale_x_continuous(limits=c(2010, 2016), breaks=c(2010:2016))


write.csv(dfsum2, file="data2.csv", row.names=FALSE)
