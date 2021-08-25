# Title     : TODO
# Objective : TODO
# Created by: Anas Marwan
# Created on: 25/8/2021

library(tidyverse)

# extract selangor, KL, Putrajaya population by district
selangor_pop <- read.csv("selangor_pop_by_district_2019.csv")
kl_pop <- read.csv("kl_pop_by_district.csv")
pj_pop <- read.csv("pj_pop_by_district.csv")
head(selangor_pop)
head(kl_pop)

drops <- c("X")
selangor_pop <-selangor_pop[ , !(names(selangor_pop) %in% drops)]
kl_pop <-kl_pop[ , !(names(kl_pop) %in% drops)]
pj_pop <-pj_pop[ , !(names(pj_pop) %in% drops)]


selangor_pop
kl_pop
pj_pop

skp_pop <- bind_rows(selangor_pop, kl_pop, pj_pop)
skp_pop   # population by district of Selangor, KL, and Putrajaya



# filter ppv list to ppv in selangor, KL, and putrajaya

ppv_list <- read.csv("ppv_all_state_with_latlong.csv")
head(ppv_list)

skp <- c("Selangor", "W.P. Kuala Lumpur", "W.P. Putrajaya")
ppv_skp <- filter(ppv_list, state %in% skp)

ppv_skp # filtered ppv_list in the three states


# changing district names in ppv_skp to the agreed names e.g. Ulu Langat -> Hulu Langat

ppv_skp["district"][ppv_skp["district"] == "Ulu Langat"] <- "Hulu Langat"
ppv_skp["district"][ppv_skp["district"] == "Ulu Selangor"] <- "Hulu Selangor"
ppv_skp["district"][ppv_skp["district"] == "Hulu Langat"] <- "Hulu Langat"

ppv_skp %>%
  group_by(state) %>%
  arrange(ppv_skp, district)

ppv_skp

# filling missing coordinate manually

ppv_skp["ppv_name"][is.na(ppv_skp["latitude"])]

#[1] "Klinik Kesihatan Batu 8"   "Menara Sime Darby Plantation (PPV OKU)"


#3.246274041679249, 101.72260142573201
ppv_skp["latitude"][ppv_skp["ppv_name"] == "Klinik Kesihatan Batu 8"] <- 3.246274041679249
ppv_skp["longitude"][ppv_skp["ppv_name"] == "Klinik Kesihatan Batu 8"] <- 101.72260142573201

# 3.1120409231145962, 101.57768062787466
ppv_skp["latitude"][ppv_skp["ppv_name"] == "Menara Sime Darby Plantation (PPV OKU)"] <- 3.1120409231145962
ppv_skp["longitude"][ppv_skp["ppv_name"] == "Menara Sime Darby Plantation (PPV OKU)"] <- 101.57768062787466

ppv_skp
ppv_skp["ppv_name"][is.na(ppv_skp["latitude"])]  # returns character(0)

ppv_skp <- group_by(state) %>%
  arrange(ppv_skp, district)


ppv_with_pop_skp <- full_join(ppv_skp, skp_pop)
ppv_with_pop_skp

write.csv(ppv_with_pop_skp, "G:/My Drive/MSTW Hackaton Team 6/ppv_with_pop_skp.csv")



