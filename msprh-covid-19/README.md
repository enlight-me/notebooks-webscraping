# MSPRH ArcGIS REST services web scraping

Web Scraping scripts for the ArcGIS REST Services diplaying a dashboard of COVID-19 pandemic in Algeria from MSPRH (Ministère de la Santé et de la réforme hospitalière algérien)

## Content

* [web-scraping-mpsrh-covid19-arcgis.ipynb](./web-scraping-mpsrh-covid19-arcgis.ipynb) jupyter notebook explaining main tasks
* [mpsrh-fetch-scheduler.py](./mpsrh-fetch-scheduler.py) web scraping script
* [msprh-fetch-scheduler.service](./msprh-fetch-scheduler.service) system service configuration file

## Setup

### For the jupyter notebooks

It is recommanded to install [Anaconda](https://www.anaconda.com/distribution/) distribution

### To run the webscraping script as a service

Install python3 dependiencies as `root`

```bash
pip3 install pandas
pip3 install apscheduler
```

Copy the `msprh-fetch-scheduler.service` file to `/lib/systemd/system/`

Enable Newly Added Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable msprh-fetch-scheduler.service
sudo systemctl start msprh-fetch-scheduler.service
```

Status of the new Service
```bash
sudo systemctl status msprh-fetch-scheduler.service
```

Sseful commands
```bash
sudo systemctl stop msprh-fetch-scheduler.service          #To stop running service 
sudo systemctl restart msprh-fetch-scheduler.service       #To start running service  
```