# Title     : TODO
# Objective : TODO
# Created by: Anas Marwan
# Created on: 25/8/2021

# WP Kuala Lumpur
district <- c("Kuala Lumpur")
pop_density <- c(7802)
pop_growth <- c(0.008)

kl_pop_by_district <- data.frame(district, pop_density, pop_growth)

kl_pop_by_district

write.csv(kl_pop_by_district,"G:/My Drive/MSTW Hackaton Team 6/kl_pop_by_district.csv")


