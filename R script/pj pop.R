# Title     : TODO
# Objective : TODO
# Created by: Anas Marwan
# Created on: 25/8/2021

# WP Putrajaya

district <- c("W.P. Putrajaya")
pop_density <- c(2063)
pop_growth <- c(0.017)

pj_pop_by_district <- data.frame(district, pop_density, pop_growth)

write.csv(pj_pop_by_district,"G:/My Drive/MSTW Hackaton Team 6/pj_pop_by_district.csv")