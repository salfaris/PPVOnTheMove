# Title     : TODO
# Objective : TODO
# Created by: Anas Marwan
# Created on: 25/8/2021

library(dplyr)
library(rvest)

#population density from DOSM 2019

# Selangor

selangor_district <- c("Petaling", "Gombak", "Klang", "Hulu Langat", "Kuala Langat", "Hulu Selangor", "Kuala Selangor", "Sabak Bernam", "Sepang")
selangor_pop_density <- c(4498, 1270, 1648, 1671, 321, 138, 215, 128, 474)  # unit: people per km
selangor_pop_growth <- c(0.015, 0.017, 0.015, 0.016, 0.017, 0.017, 0.017, 0.017, 0.017)  # annually

selangor_pop_by_district <- data.frame(selangor_district, selangor_pop_density, selangor_pop_growth)

selangor_pop_by_district

# write.csv(selangor_pop_by_district,"G:/My Drive/MSTW Hackaton Team 6/selangor_pop_by_district_2019.csv")

