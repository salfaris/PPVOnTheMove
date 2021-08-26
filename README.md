# YMEHack2021
Repository for YME's MSTW Hackathon 2021

## 🚑 PPV On The Move
PPV on the move, instant vroom vroom with Unitroid

### 🚑 What is PPV On The Move?
PPV On The Move is an AI-driven project that utilise the *Uniform Centroid Algorithm (Unitroid)* that we developed to suggest strategic spots to place the PPV pop up centres. This project is purposed to help the government in improving the vaccination distribution that costs less time, with increased efficiency, backed by data and statistics.


### 💡 Our Motivation
- 🚗 Increase reachability - Vaccines are for all and should be accessible by everyone from every nook and cranny.
- 🚶‍♂️ Reduce overcrowding at centres - By having portable PPVs, people from various places would not need to gather at one small place and are able to practice social distancing. Ditch the long queues, and get vaccinated in an instant.
- 📐 A more reliable approach - Our approach is heavily backed up by data. This helps the government in making better decisions on where to open PPV to facilitate the recovery plan for Malaysia.


### 📋 Our Methods
This project was heavily relied on data. We decide to choose Selangor, W.P. Kuala Lumpur, and W.P. Putrajaya as point of reference for this project.
- ✂️ Data Scraping - We collected information of each PPV of the chosen states, categorised by districts scraped from the JKJAV portal. With resources provided by Department of Statistics Malaysia (DOSM), we are able to obtain information of population density for each district in every state in Malaysia.
- 💻 Data Processing - We matched each PPV with its district, state, coordinates, and population density. This allows us to estimate the reachability of each existing PPV and picture them at the district and state level. With this piece of information, our own developed *Unitroid* algorithm can further suggest any region with less degree of reachability to the existing PPVs.


### 💡 How Does Unitroid Work?
As the name *Uniform Centroid* suggests, the *Unitroid algorithm* uses geometry to find potential PPV pop up centres by sampling current PPVs uniformly (i.e. in a uniform distribution fashion) and computing their centroid. Our hypothesis is that centroids arising in this way are suitable candidates to place pop up PPVs since it fills the PPV void in the state, allowing for better access to vaccines for those feeling burdened having to travel to current PPVs. Moreover, our experiments have shown that centroids drawn from the *Unitroid algorithm* gives rise to a natural path for PPV pop up centres to follow which reduces usage of resources.
